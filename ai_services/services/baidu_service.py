import requests
from django.conf import settings
from .ai_config import BaiduAIConfig

class BaiduAIService:
    def __init__(self):
        self.api_key = settings.BAIDU_API_KEY
        self.secret_key = settings.BAIDU_SECRET_KEY
        self.base_url = "https://aip.baidubce.com"
        self.access_token = None

    def _get_access_token(self):
        """Get access token from Baidu using API key and secret key"""
        url = f"{self.base_url}/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        
        try:
            response = requests.post(url, params=params)
            result = response.json()
            
            if 'access_token' in result:
                return result['access_token']
            else:
                raise Exception(f"Failed to get access token: {result}")
                
        except Exception as e:
            print(f"Error getting access token: {str(e)}")
            return None

    def _make_api_call(self, prompt):
        if not self.access_token:
            return None
            
        # Use the exact URL format that worked in Postman
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token={self.access_token}"
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.3,  # Lower temperature for more focused output
            'top_p': 0.5,       # More focused token selection
            'penalty_score': 1.2,
            'system': "你是一位在中国的医生，正在对病人进行随访。请用简洁的2-3句话总结随访记录的要点，重点关注病情变化和治疗效果。",
            'stream': False,
            'stop': ["结束", "完成"],  # Optional stop words
            'max_output_tokens': 150,  # Limit output length
            'frequency_penalty': 0.3,   # Reduce repetition
            'presence_penalty': 0.1,    # Encourage some novelty
            'metadata': {
                'source': 'followup_system',
                'type': 'medical_notes'
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
        
            # Check rate limits
            remaining_requests = int(response.headers.get('X-Ratelimit-Remaining-Requests', 0))
            remaining_tokens = int(response.headers.get('X-Ratelimit-Remaining-Tokens', 0))
        
            if remaining_requests <= 1 or remaining_tokens <= 100:
                print(f"Warning: API rate limits approaching. Requests: {remaining_requests}, Tokens: {remaining_tokens}")
            
            return response.json()
        except Exception as e:
            print(f"Error making API call: {str(e)}")
            return None
        
    def _format_messages(self, prompt):
        """Format prompt into proper message structure"""
        return [
            {
                'role': 'user',
                'content': prompt
            }
        ]

    def _handle_response(self, response):
        """Handle the API response and extract relevant information"""
        try:
            if not response:
                raise ValueError("No response received")

            # Check for basic response structure
            if 'result' not in response:
                raise ValueError("No result in API response")

            # Extract important fields
            result = {
                'content': response.get('result', ''),           # The actual AI response
                'id': response.get('id', ''),                    # Conversation ID
                'is_truncated': response.get('is_truncated', False),  # If response was cut off
                'need_clear_history': response.get('need_clear_history', False),  # Security check
                'usage': response.get('usage', {})               # Token usage stats
            }

            # Log if there are security concerns
            if result['need_clear_history']:
                print(f"Security warning for conversation {result['id']}: History should be cleared")
                
            # Log if response was truncated
            if result['is_truncated']:
                print(f"Warning: Response was truncated for conversation {result['id']}")

            # Extract and log usage statistics
            usage = result['usage']
            if usage:
                print(f"API Usage Stats:")
                print(f"- Prompt tokens: {usage.get('prompt_tokens', 0)}")
                print(f"- Completion tokens: {usage.get('completion_tokens', 0)}")
                print(f"- Total tokens: {usage.get('total_tokens', 0)}")
                
                # Log usage to database
                self._log_usage(
                    conversation_id=result['id'],
                    prompt_tokens=usage.get('prompt_tokens', 0),
                    completion_tokens=usage.get('completion_tokens', 0),
                    total_tokens=usage.get('total_tokens', 0)
                )

            # Return the actual content for the notetaking system
            return result['content']

        except Exception as e:
            print(f"Error processing AI response: {str(e)}")
            return None

    def _log_usage(self, conversation_id, prompt_tokens, completion_tokens, total_tokens):
        """Log token usage to database"""
        try:
            from ai_services.models import AIUsageLog
            
            AIUsageLog.objects.create(
                service='baidu',
                endpoint='ernie-lite-8k',
                tokens_used=total_tokens,
                metadata={
                    'conversation_id': conversation_id,
                    'prompt_tokens': prompt_tokens,     # Number of tokens in the input
                    'completion_tokens': completion_tokens,  # Number of tokens in the AI's response
                    'total_tokens': total_tokens        # Total tokens used
                }
            )
        except Exception as e:
            print(f"Error logging API usage: {str(e)}")


    def process_followup_notes(self, notetaking_obj):
        # Process followup notes using Baidu AI
        if not self.access_token:
            self.access_token = self._get_access_token()

        prompt = BaiduAIConfig.NOTE_PROCESSING_PROMPT.format(
            original_notes=notetaking_obj.raw_notes
        )

        # Make API call and process response
        response = self._make_api_call(prompt)
        processed_result = self._handle_response(response)

        if processed_result:
            notetaking_obj.processed_notes = processed_result
            notetaking_obj.save()
            return True, notetaking_obj

        return False, "Failed to process notes"
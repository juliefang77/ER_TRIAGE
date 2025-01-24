import requests
from django.conf import settings
from ai_services.serializers.survey_serializer import SurveyLLMAnalysisSerializer
from followup.models import FollowupRecipient, SurveyAi
import json
from .ai_config import BaiduAIConfig

class SurveyAnalysisService:
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
            
        url = f"{self.base_url}/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token={self.access_token}"
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.3,
            'top_p': 0.5,
            'penalty_score': 1.2,
            'system': "你是一位在中国的医生，正在分析多位病人的随访问卷。请总结他们的恢复情况，指出需要特别关注的问题，并提出后续随访建议。",
            'stream': False,
            'stop': ["结束", "完成"],
            'max_output_tokens': 800,  # Increased for multiple surveys
            'frequency_penalty': 0.3,
            'presence_penalty': 0.1,
            'metadata': {
                'source': 'followup_system',
                'type': 'survey_analysis'
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            remaining_requests = int(response.headers.get('X-Ratelimit-Remaining-Requests', 0))
            remaining_tokens = int(response.headers.get('X-Ratelimit-Remaining-Tokens', 0))
        
            if remaining_requests <= 1 or remaining_tokens <= 100:
                print(f"Warning: API rate limits approaching. Requests: {remaining_requests}, Tokens: {remaining_tokens}")
            
            return response.json()
        except Exception as e:
            print(f"Error making API call: {str(e)}")
            return None


    def _handle_response(self, response):
        # """Handle the API response and extract relevant information"""
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

            # Return the actual content for the survey analysis system
            return result['content']

        except Exception as e:
            print(f"Error processing AI response: {str(e)}")
            return None
    
    def analyze_surveys(self, recipient_ids):
        """Process survey analysis and return result without saving"""
        if not self.access_token:
            self.access_token = self._get_access_token()

       # Get recipients data with all needed relations
        recipients = FollowupRecipient.objects.filter(
            id__in=recipient_ids,
            survey_status='YES_RESPONSE'
        ).select_related(
            'patient',
            'triage_record'
        ).prefetch_related(
            'surveys__template',  # Using correct related_name 'surveys'
            'surveys__response'
        )

        # Format data for prompt
        surveys_data = SurveyLLMAnalysisSerializer(recipients, many=True).data
        prompt = BaiduAIConfig.SURVEY_ANALYSIS_PROMPT.format(
            surveys=json.dumps(surveys_data, ensure_ascii=False, indent=2)
        )

        # Make API call and process response
        response = self._make_api_call(prompt)
        print(f"API Response: {response}")  # Debug log
        processed_result = self._handle_response(response)
        print(f"Processed result: {processed_result}")  # Debug log

        if processed_result:
            return True, {
                'analysis_result': processed_result,
                'recipient_ids': recipient_ids
            }

        return False, "Failed to process survey analysis"


    def save_analysis(self, analysis_result, recipient_ids, analysis_name, hospital):
        """Save the analysis result if user chooses to keep it"""
        try:
            survey_ai = SurveyAi.objects.create(
                hospital=hospital,
                analysis_name=analysis_name,
                analysis_result=analysis_result
            )
            # Add recipients to the analysis
            survey_ai.recipients.add(*recipient_ids)
            return True, survey_ai
        except Exception as e:
            return False, str(e)


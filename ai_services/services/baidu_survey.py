import requests
from django.conf import settings
from ai_services.serializers.survey_serializer import SurveyLLMAnalysisSerializer
from followup.models import FollowupSurvey
import json

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
            'max_output_tokens': 300,  # Increased for multiple surveys
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

    def analyze_surveys(self, recipient_ids, prompt_template):
        """Main method to analyze surveys"""
        # Get access token first
        self.access_token = self._get_access_token()
        if not self.access_token:
            return None

        # Get survey data
        surveys = FollowupSurvey.objects.filter(
            recipient__id__in=recipient_ids,
            recipient__survey_status='YES_RESPONSE'
        ).select_related(
            'recipient__patient',
            'recipient__triage_record',
            'template'
        )
        surveys_data = SurveyLLMAnalysisSerializer(surveys, many=True).data
        
        # Format prompt with survey data
        prompt = prompt_template.format(
            surveys=json.dumps(surveys_data, ensure_ascii=False, indent=2)
        )
        
        # Make API call
        return self._make_api_call(prompt)


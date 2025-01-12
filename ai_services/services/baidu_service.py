from django.conf import settings
import requests
from .ai_config import BaiduAIConfig

class BaiduAIService:
    def __init__(self):
        self.api_key = settings.BAIDU_API_KEY
        self.secret_key = settings.BAIDU_SECRET_KEY
        self.base_url = "https://aip.baidubce.com"
        self.access_token = None

    def process_followup_notes(self, notetaking_obj):
        """
        Process followup notes using Baidu AI
        """
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
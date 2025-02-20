from typing import Dict, Any
from dataclasses import dataclass
import requests
import json

@dataclass
class SocialSecurityCardInfo:
    """Structured Social Security Card information"""
    ssc_card_number: str          # 卡号
    ssc_name: str                 # 姓名
    ssc_gender: str               # 性别 (changed from sex to gender for consistency)
    ssc_social_number: str        # 社会保障卡号 (shortened from security for brevity)
    ssc_birth_date: str           # 出生日期
    ssc_issue_date: str           # 签发日期
    ssc_bank_number: str          # 银行卡号
    ssc_expiry_date: str          # 有效期限

class SocialSecurityReader:
    def __init__(self, api_key: str, secret_key: str):
        """Initialize with Baidu API credentials"""
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/social_security_card"

    # ... previous get_access_token and read_card_base64 methods remain the same ...
    def get_access_token(self) -> str:
        """Get access token from Baidu API"""
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()['access_token']
        else:
            raise Exception("Failed to get access token")

    def read_card_base64(self, base64_string: str) -> Dict[str, Any]:
        """Read social security card from base64 string"""
        access_token = self.get_access_token()

        data = {
            'image': base64_string
        }

        response = requests.post(
            f"{self.api_url}?access_token={access_token}",
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.ok:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.text}")

    def extract_card_info(self, response: Dict[str, Any]) -> SocialSecurityCardInfo:
        """Extract structured information from API response"""
        words_result = response.get('words_result', {})
        
        return SocialSecurityCardInfo(
            ssc_card_number=words_result.get('card_number', {}).get('words', ''),
            ssc_name=words_result.get('name', {}).get('words', ''),
            ssc_gender=words_result.get('sex', {}).get('words', ''),
            ssc_social_number=words_result.get('social_security_number', {}).get('words', ''),
            ssc_birth_date=words_result.get('birth_date', {}).get('words', ''),
            ssc_issue_date=words_result.get('issue_date', {}).get('words', ''),
            ssc_bank_number=words_result.get('bank_card_number', {}).get('words', ''),
            ssc_expiry_date=words_result.get('expiry_date', {}).get('words', '')
        )

    def process_card(self, base64_string: str) -> Dict[str, Any]:
        """
        Process social security card and return flattened response
        """
        try:
            # Get raw response from API
            response = self.read_card_base64(base64_string)
            
            # Extract card info
            card_info = self.extract_card_info(response)
            
            # Return flattened structure
            return {
                'success': True,
                'error': None,
                'log_id': response.get('log_id', ''),
                'direction': response.get('direction', 0),
                'ssc_card_number': card_info.ssc_card_number,
                'ssc_name': card_info.ssc_name,
                'ssc_gender': card_info.ssc_gender,
                'ssc_social_number': card_info.ssc_social_number,
                'ssc_birth_date': card_info.ssc_birth_date,
                'ssc_issue_date': card_info.ssc_issue_date,
                'ssc_bank_number': card_info.ssc_bank_number,
                'ssc_expiry_date': card_info.ssc_expiry_date
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'log_id': '',
                'direction': 0,
                'ssc_card_number': '',
                'ssc_name': '',
                'ssc_gender': '',
                'ssc_social_number': '',
                'ssc_birth_date': '',
                'ssc_issue_date': '',
                'ssc_bank_number': '',
                'ssc_expiry_date': ''
            }
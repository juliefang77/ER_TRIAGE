from typing import Dict, Any
from dataclasses import dataclass
import requests
import json

@dataclass
class IDCardInfo:
    """Structured ID card information (front side only)"""
    id_name: str
    id_number: str
    id_gender: str
    id_nationality: str
    id_birth_date: str
    id_address: str

class IDCardReader:
    def __init__(self, api_key: str, secret_key: str):
        """Initialize with Baidu API credentials"""
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard"

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

    def read_id_card_base64(self, base64_string: str) -> Dict[str, Any]:
        """Read ID card from base64 string"""
        access_token = self.get_access_token()

        data = {
            'image': base64_string,
            'id_card_side': 'front',
            'detect_risk': 'true',
            'detect_quality': 'true'
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

    def extract_card_info(self, response: Dict[str, Any]) -> IDCardInfo:
        """Extract structured information from API response"""
        words_result = response.get('words_result', {})
        
        return IDCardInfo(
            id_name=words_result.get('姓名', {}).get('words', ''),
            id_number=words_result.get('公民身份号码', {}).get('words', ''),
            id_gender=words_result.get('性别', {}).get('words', ''),
            id_nationality=words_result.get('民族', {}).get('words', ''),
            id_birth_date=words_result.get('出生', {}).get('words', ''),
            id_address=words_result.get('住址', {}).get('words', '')
        )

    def validate_card_quality(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Validate card quality and authenticity"""
        quality_issues = []
        
        risk_type = response.get('risk_type')
        if risk_type and risk_type != 'normal':
            quality_issues.append(f"Risk detected: {risk_type}")
            
        card_quality = response.get('card_quality', {})
        if card_quality:
            if card_quality.get('IsClear') == 0:
                quality_issues.append("Image is not clear")
            if card_quality.get('IsComplete') == 0:
                quality_issues.append("Card edges not complete")

        return {
            'is_valid': len(quality_issues) == 0,
            'issues': quality_issues
        }

    def process_id_card(self, base64_string: str) -> Dict[str, Any]:
        """
        Process ID card and return flattened response
        """
        try:
            # Get raw response from API
            response = self.read_id_card_base64(base64_string)
            
            # Extract card info
            card_info = self.extract_card_info(response)
            
            # Validate quality
            quality = self.validate_card_quality(response)
            
            # Return flattened structure
            return {
                'success': True,
                'error': None,
                'is_valid': quality['is_valid'],
                'quality_issues': quality['issues'],
                'id_name': card_info.id_name,
                'id_number': card_info.id_number,
                'id_gender': card_info.id_gender,
                'id_nationality': card_info.id_nationality,
                'id_birth_date': card_info.id_birth_date,
                'id_address': card_info.id_address,
                'id_validation_type': response.get('idcard_number_type', -1)  # Added this line
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'is_valid': False,
                'quality_issues': [],
                'id_name': '',
                'id_number': '',
                'id_gender': '',
                'id_nationality': '',
                'id_birth_date': '',
                'id_address': '',
                'id_validation_type': -1
            }

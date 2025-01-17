class BaiduAIConfig:
    '''FOLLOWUP_PARAMS = {
        'temperature': 0.7,
        'max_tokens': 1000,
        'top_p': 0.9,
    }'''
    
    NOTE_PROCESSING_PROMPT = """
    请根据以下随访记录进行整理和扩展:
    {original_notes}

    要求：
    1. 扩展现有笔记，使其更加完整和专业
    2. 按以下格式整理：
       - 恢复情况：
       - 用药情况：
       - 其他注意事项：
    3. 如果以上三点不存在，就写“无”，不要编造
    """

# followup/prompts/survey_analysis_prompts.py

class SurveyAnalysisPrompts:
    BASE_PROMPT = """
    请分析以下患者的随访问卷回复:
    {surveys}
    
    请提供:
    1. 患者恢复情况总结
    2. 需要特别关注的问题
    3. 建议的后续随访行动
    """
    
    @classmethod
    def get_prompt(cls):
        return cls.BASE_PROMPT
class BaiduAIConfig:
    FOLLOWUP_PARAMS = {
        'temperature': 0.7,
        'max_tokens': 1000,
        'top_p': 0.9,
    }
    
    NOTE_PROCESSING_PROMPT = """
    请根据以下随访记录进行整理和扩展:
    {original_notes}

    要求：
    1. 扩展现有笔记，使其更加完整和专业
    2. 按以下格式整理：
       - 恢复情况：
       - 用药情况：
       - 其他注意事项：
    3. 使用简洁、专业的医疗用语
    4. 保持语言精炼，直击重点
    """
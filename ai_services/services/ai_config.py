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

    SURVEY_ANALYSIS_PROMPT = """
    请分析以下患者的随访问卷调查结果。整理成格式如下的文字：
    1. 患者的专科类型分布：
    2. 恢复情况分布：
    3. 用药情况：
    4. 是否加重、有副作用：
    5. 复诊需求总结：

    问卷数据：
    {surveys}
    
    请用中文给出符合上述5点格式的分析结果
    """
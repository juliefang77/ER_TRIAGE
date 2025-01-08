from django.db import models

class StandardQuestion(models.Model):
    QUESTION_CATEGORY_CHOICES = [
        ('GENERAL', '一般情况'),
        ('SYMPTOMS', '症状'),
        ('MEDICATION', '用药'),
        ('RECOVERY', '恢复情况'),
        ('SPECIAL_DISEASE', '特殊疾病相关')
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('TEXT', '文本'),
        ('YES_NO', '是否'),
        ('SINGLE_CHOICE', '单选'),
        ('RATING', '评分')
    ]

    question_text = models.CharField(
        max_length=500,
        verbose_name='问卷问题',
        null=True,
        blank=True
    )

    question_category = models.CharField(
        max_length=50,
        choices=QUESTION_CATEGORY_CHOICES,
        verbose_name='问题分类',
        null=True,
        blank=True
    )

    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        verbose_name='问题格式',
        null=True,
        blank=True
    )

    choice_one = models.CharField(
        max_length=200,
        verbose_name='选项一',
        null=True,
        blank=True
    )

    choice_two = models.CharField(
        max_length=200,
        verbose_name='选项二',
        null=True,
        blank=True
    )

    choice_three = models.CharField(
        max_length=200,
        verbose_name='选项三',
        null=True,
        blank=True
    )

    choice_four = models.CharField(
        max_length=200,
        verbose_name='选项四',
        null=True,
        blank=True
    )

    choice_five = models.CharField(
        max_length=200,
        verbose_name='选项五',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='是否启用',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = '标准问题'
        verbose_name_plural = '标准问题'

    def __str__(self):
        return self.question_text or '未命名问题'


# StandardQuestion Table Relations:
    # - Used in many SurveyTemplates (ManyToMany through reverse relation)
    # - Has many SurveyResponses (reverse relation)
    #
    # Fields:
    # 1. question_text | 问卷问题 | CharField
    # 2. question_category | 问题分类 | CharField (choices)
    # 3. question_type | 问题格式 | CharField (choices)
    # 4. choice_one | 选项一 | CharField
    # 5. choice_two | 选项二 | CharField
    # 6. choice_three | 选项三 | CharField
    # 7. choice_four | 选项四 | CharField
    # 8. choice_five | 选项五 | CharField
    # 9. is_active | 是否启用 | BooleanField
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
FollowupRecordDisplayViewSet, 
AddToFollowupViewSet, 
StandardQuestionViewSet, 
SurveyTemplateViewSet, 
SystemTemplateViewSet, 
MassSendSurveyViewSet, 
ManagementSurveyHistoryViewSet,
MassSendMessageViewSet,
SurveyTemplateSearchViewSet
)

router = DefaultRouter()

# Register without the apifollowup prefix since it's handled in global urls.py
router.register(
    r'display', FollowupRecordDisplayViewSet, basename='saas-followup-display')

# Select multiple patients, and add them to 随访计划
router.register(
    r'management', AddToFollowupViewSet, basename='saas-followup-management')

# 查看所有question bank里的问题，drag and pull 制作问卷
router.register(r'standard-questions', StandardQuestionViewSet, basename='standard-questions')

# 查看已创建的templates
router.register(r'survey-templates', SurveyTemplateViewSet, basename='survey-templates')

# 系统预设的templates
router.register(r'system-templates', SystemTemplateViewSet, basename='system-templates')

# 群发系统生成的surveys
router.register(r'mass-survey', MassSendSurveyViewSet, basename='mass-survey')

 # 查看已经填写的surveys
router.register(r'management-surveys-history', ManagementSurveyHistoryViewSet, basename='management-survey-history' )

# 群发前端传给Django content 的notification message
router.register(r'mass-message', MassSendMessageViewSet, basename='mass-message')

# 人工发送问卷页面，左上角“选择问卷模版” search function
router.register(r'template-search', SurveyTemplateSearchViewSet, basename='template-search')

urlpatterns = [
    path('', include(router.urls)),
]
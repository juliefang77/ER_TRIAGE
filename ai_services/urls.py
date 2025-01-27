from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AIFollowupNotesViewSet, SurveyAnalysisViewSet, SurveyAnalysisListViewSet, AiNotesListViewSet

router = DefaultRouter()

# AI 处理一个患者的随访笔记
router.register(r'followup-notes', AIFollowupNotesViewSet, basename='ai-followup-notes')

# AI 已处理的notes list page
router.register(r'ai-notes-list', AiNotesListViewSet, basename='ai-notes-list')

# AI 批量处理surveys
router.register(r'ai-survey', SurveyAnalysisViewSet, basename='ai-survey')

# AI 已处理的surveys list page
router.register(r'ai-survey-page', SurveyAnalysisListViewSet, basename='ai-survey-page')

urlpatterns = [
    path('', include(router.urls)),
]
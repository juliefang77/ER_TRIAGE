from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AIFollowupNotesViewSet, SurveyAnalysisViewSet

router = DefaultRouter()

# AI 处理一个患者的随访笔记
router.register(r'followup-notes', AIFollowupNotesViewSet, basename='ai-followup-notes')
router.register(r'ai-survey', SurveyAnalysisViewSet, basename='ai-survey')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from .views import RegisterView, TranscriptUploadView, EvaluateTranscriptView, EvaluationDetailView, EvaluationListView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('transcripts/', TranscriptUploadView.as_view(), name='transcript-upload'),
    path('transcripts/<int:transcript_id>/evaluate/', EvaluateTranscriptView.as_view(), name='evaluate'),
    path('evaluations/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation-detail'),
    path('evaluations/', EvaluationListView.as_view(), name='evaluation-list'),
]
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Transcript, Evaluation
from .serializers import RegisterSerializer, TranscriptUploadSerializer, EvaluationSerializer
from .permissions import IsAdminOrReviewer, CanUploadTranscript
from .utils import generate_evaluation

from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class TranscriptUploadView(generics.CreateAPIView):
    serializer_class = TranscriptUploadSerializer
    permission_classes = [CanUploadTranscript]

    def get_serializer_context(self):
        return {'request': self.request}


class EvaluateTranscriptView(APIView):
    permission_classes = [IsAdminOrReviewer]

    def post(self, request, transcript_id):
        try:
            transcript = Transcript.objects.get(id=transcript_id)
        except Transcript.DoesNotExist:
            return Response({"detail": "Transcript not found."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(transcript, 'evaluation'):
            return Response({"detail": "Transcript already evaluated."}, status=status.HTTP_400_BAD_REQUEST)

        comm, tech, prob, summary = generate_evaluation(transcript.content)
        evaluation = Evaluation.objects.create(
            transcript=transcript,
            communication_score=comm,
            technical_accuracy_score=tech,
            problem_solving_score=prob,
            summary=summary,
        )
        return Response(EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED)


class EvaluationDetailView(generics.RetrieveAPIView):
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'reviewer']:
            return Evaluation.objects.all()
        return Evaluation.objects.filter(transcript__uploaded_by=user)


class EvaluationListView(generics.ListAPIView):
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Evaluation.objects.all() if user.role in ['admin', 'reviewer'] else Evaluation.objects.filter(transcript__uploaded_by=user)

        interviewer = self.request.query_params.get('interviewer')
        candidate = self.request.query_params.get('candidate')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if interviewer:
            qs = qs.filter(transcript__uploaded_by__username=interviewer)
        if candidate:
            qs = qs.filter(transcript__candidate__name__icontains=candidate)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs
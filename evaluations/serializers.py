from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Candidate, Transcript, Evaluation

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):
        user = User(username=validated_data['username'], role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TranscriptUploadSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(write_only=True)
    candidate_email = serializers.EmailField(write_only=True)
    position_applied = serializers.CharField(write_only=True)

    class Meta:
        model = Transcript
        fields = ['id', 'content', 'candidate_name', 'candidate_email', 'position_applied', 'created_at']

    def create(self, validated_data):
        candidate = Candidate.objects.create(
            name=validated_data.pop('candidate_name'),
            email=validated_data.pop('candidate_email'),
            position_applied=validated_data.pop('position_applied'),
        )
        transcript = Transcript.objects.create(
            candidate=candidate,
            uploaded_by=self.context['request'].user,
            content=validated_data['content'],
        )
        return transcript


class EvaluationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='transcript.candidate.name', read_only=True)
    candidate_email = serializers.CharField(source='transcript.candidate.email', read_only=True)
    transcript_content = serializers.CharField(source='transcript.content', read_only=True)
    interviewer = serializers.CharField(source='transcript.uploaded_by.username', read_only=True)

    class Meta:
        model = Evaluation
        fields = ['id', 'candidate_name', 'candidate_email', 'transcript_content',
                  'interviewer', 'communication_score', 'technical_accuracy_score',
                  'problem_solving_score', 'summary', 'created_at']
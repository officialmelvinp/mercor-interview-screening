from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('interviewer', 'Interviewer'),
        ('reviewer', 'Reviewer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    position_applied = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transcript(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='transcripts')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transcripts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Evaluation(models.Model):
    transcript = models.OneToOneField(Transcript, on_delete=models.CASCADE, related_name='evaluation')
    communication_score = models.FloatField()
    technical_accuracy_score = models.FloatField()
    problem_solving_score = models.FloatField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
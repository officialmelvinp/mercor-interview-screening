from django.contrib import admin
from .models import User, Candidate, Transcript, Evaluation

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Transcript)
admin.site.register(Evaluation)
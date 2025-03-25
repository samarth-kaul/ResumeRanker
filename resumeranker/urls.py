from django.urls import path
from django.shortcuts import render
from .views import JobDescriptionAPI, AnalyzeResumeAPI, index
# from . import views

urlpatterns = [
    # path('', lambda request: render(request, 'resumeranker/templates/index.html'), name='upload-resume'),
    path('', index, name='home'),
    path('api/jobs/', JobDescriptionAPI.as_view(), name='job-descriptions'),
    path('api/resume/', AnalyzeResumeAPI.as_view(), name='analyze-resume'),
]

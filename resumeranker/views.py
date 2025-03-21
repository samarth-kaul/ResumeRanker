from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import JobDescription, Resume
from .serializer import JobDescriptionSerializer, ResumeSerializer
from .analyzer import process_resume

class JobDescriptionAPI(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many = True)
        return Response({
            'status' : True,
            'data' : serializer.data
        })

class AnalyzeResumeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data.get('job_description'):
                return Response({
                    'status' : False,
                    'message' : 'job_description is required',
                    'data' : {}
                })
            
            serialzier = ResumeSerializer(data = data)
            if not serialzier.is_valid():
                return Response({
                    'status' : False,
                    'message' : 'errors',
                    'data' : serialzier.errors
                })
            
            serialzier.save()
            _data = serialzier.data
            resume_instance = Resume.objects.get(id = _data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path, JobDescription.objects.get(id = data.get('job_description')).job_description)
            # print(resume_path)
            return Response({
                        'status' : True,
                        'message' : 'Resume Analyzed!',
                        'data' : {}
                    })
    
        except Exception as e:
            return Response({
                'data' : False
            })

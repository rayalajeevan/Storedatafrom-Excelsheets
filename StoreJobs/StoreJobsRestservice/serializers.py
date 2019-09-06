from rest_framework import  serializers
from .models import WebCompanyJobs,WebInternshipJobs
class WebCompanyJobsSerilizer(serializers.ModelSerializer):
    class Meta:
        model=WebCompanyJobs
        fields='__all__'
    def create(self, validated_data):
        return WebCompanyJobs.objects.create(**validated_data)
class WebInternshipJobsSerilizer(serializers.ModelSerializer):
    class Meta:
        model=WebInternshipJobs
        fields='__all__'
    def create(self, validated_data):
        return WebInternshipJobs.objects.create(**validated_data)        

from rest_framework import serializers
from locationModifier.models import Web_company_jobs,Web_internships_jobs

class WebCompanyJobsserializer(serializers.ModelSerializer):
    class Meta:
        model=Web_company_jobs
        fields="__all__"
class WebInternshipsJobsserializer(serializers.ModelSerializer):
    class Meta:
        model=Web_internships_jobs
        fields='__all__'
class WebInternshipsCOUNTJobsserializer(serializers.ModelSerializer):
    class Meta:
        model=Web_internships_jobs
        fields=('company_info_id','dcount','tested_status','scrappedBy','company_name')       
class WebCompanyCOUNTJobsserializer(serializers.ModelSerializer):
    class Meta:
        model=Web_company_jobs
        fields=('company_info_id','dcount','tested_status','scrappedBy','company_name',)
from rest_framework import serializers
from locationModifier.models import *

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
        model=Web_internships_jobs_forSerlize
        fields=('company_info_id','dcount','tested_status','scrappedBy','company_name')       
class WebCompanyCOUNTJobsserializer(serializers.ModelSerializer):
    class Meta:
        model=Web_company_jobs_forSerlize
        fields=('company_info_id','dcount','tested_status','scrappedBy','company_name',)
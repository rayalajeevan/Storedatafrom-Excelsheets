from rest_framework import serializers
from companyapp.models import CompanyInfo,Industries

class CompanyInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model=CompanyInfo
        fields=('company_info_id',
        'company_name','company_size',
        'company_contact','company_website',
        'company_unique_id','hq_locations_location',
        'hq_company_address_line1',
        'hq_company_address_line2','industry','estd_year')
    def update(self,instance,validated_data):
        fields=('company_info_id',
        'company_name','company_size',
        'company_contact','company_website',
        'company_unique_id','hq_locations_location',
        'hq_company_address_line1',
        'hq_company_address_line2','industry','estd_year')
        for key in fields:
            instance.__dict__[key]=validated_data.get(key,instance.__dict__.get(key))
        instance.save()
        return instance
class IndustriesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Industries
        fields='__all__'
        

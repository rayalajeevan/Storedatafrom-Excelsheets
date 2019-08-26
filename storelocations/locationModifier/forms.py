from django import forms
from .models import company_infoCopy
from copy import deepcopy
class UploadFiles(forms.Form):
    unique_obj=company_infoCopy.objects.latest('company_info_id')
    unique=int(unique_obj.company_unique_id[1::])+1
    unique=unique_obj.company_unique_id[0]+str(unique)
    company_name = forms.CharField()
    company_size = forms.CharField()
    company_website = forms.CharField()
    company_logo_path = forms.CharField()
    company_contact = forms.CharField()
    hq_locations_location_id=forms.CharField(widget=forms.TextInput(attrs={'id':'locationId'}))
    company_profile_description = forms.CharField()
    image_purity = forms.CharField()
    estd_year = forms.CharField()
    company_unique_id=forms.CharField(initial=unique)
    hq_company_address_line1 = forms.CharField()
    hq_company_address_line2 = forms.CharField()

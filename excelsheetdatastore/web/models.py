from django.db import models
from django.utils.encoding import python_2_unicode_compatible
class Beautify_company_jobs(models.Model):
    class Meta:
        db_table='beautify_company_jobs'
        
    beautify_company_id=models.BigIntegerField(primary_key=True)
    company_info_id=models.IntegerField()
    instruction_id=models.IntegerField()
@python_2_unicode_compatible
class web_internship_jobs(models.Model):
    class Meta:
        db_table='web_internship_jobs'
        
    web_internship_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100,default=None)
    company_info_id=models.CharField(max_length=100,default=None)
    other_locations=models.CharField(max_length=1000,default=None)
    job_title=models.CharField(max_length=255,default=None)
    job_description=models.TextField(default=None)
    scrapped_location=models.TextField(default=None)
    company_name=models.CharField(max_length=255,default=None)
    job_location=models.TextField(default=None)
    apply_link=models.TextField(default=None)
    posted_date=models.DateTimeField(default=None)
    qualifications=models.TextField(default=None)
    job_type=models.CharField(max_length=100,default=None)
    schedule_job_timings=models.CharField(max_length=100,default=None)
    industry_type=models.CharField(max_length=50,default=None)
    experience=models.CharField(max_length=500,default=None)
    job_expired_date=models.CharField(max_length=100,default=None)
    functional_area=models.CharField(max_length=100,default=None)
    salary_compensation=models.CharField(max_length=200,default=None)
    travel_requirement=models.CharField(max_length=100,default=None)
    employer=models.CharField(max_length=100,default=None)
    organization_type=models.CharField(max_length=100,default=None)
    company_type_relation=models.CharField(max_length=100,default=None)
    FLSA_status=models.CharField(max_length=100,default=None)
    job_roles_responsibilities=models.TextField(default=None)
    related_jobs=models.CharField(max_length=200,default=None)
    web_creative_services=models.CharField(max_length=100,default=None)
    job_questions=models.TextField(default=None)
    job_requirements=models.TextField(default=None)
    weekly_hours=models.CharField(max_length=10,default=None)
    opportunities=models.CharField(max_length=200,default=None)
    available_time=models.CharField(max_length=55,default=None)
    discipline=models.CharField(max_length=255,default=None)
    work_shift=models.CharField(max_length=200,default=None)
    relocation_available=models.CharField(max_length=50,default=None)
    ITAR=models.CharField(max_length=255,default=None)
    company_description=models.TextField(default=None)
    selection_process=models.CharField(max_length=100,default=None)
    employee_status=models.CharField(max_length=100,default=None)
    company_level=models.CharField(max_length=100,default=None)
    job_tracking_code=models.CharField(max_length=20,default=None)
    travel_allowance=models.CharField(max_length=55,default=None)
    skills_preferred=models.CharField(max_length=500,default=None)
    skills_required=models.TextField(default=None)
    employer_email=models.CharField(max_length=100,default=None)
    employer_contact=models.CharField(max_length=20,default=None)
    enquiry_details=models.CharField(max_length=200,default=None)
    important_notes=models.TextField(default=None)
    country_type=models.CharField(max_length=50,default=None)
    scrapped_date=models.DateTimeField(default=None)
    scrappedBy=models.CharField(max_length=50,default=None)
    scrapped_location=models.TextField(default=None)
    deleted_status=models.TextField(default=None)

@python_2_unicode_compatible
class company_jobs(models.Model):
    class Meta:
        db_table='web_company_jobs'
        
    web_company_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100,default=None)
    company_info_id=models.CharField(max_length=100,default=None)
    job_title=models.CharField(max_length=255,default=None)
    scrapped_location=models.TextField(default=None)
    scrapped_location=models.TextField(default=None)
    job_description=models.TextField(default=None)
    company_name=models.CharField(max_length=255,default=None)
    other_locations=models.CharField(max_length=1000,default=None)
    job_location=models.TextField(default=None)
    apply_link=models.TextField(default=None)
    posted_date=models.DateTimeField(default=None)
    qualifications=models.TextField(default=None)
    job_type=models.CharField(max_length=100,default=None)
    schedule_job_timings=models.CharField(max_length=100,default=None)
    industry_type=models.CharField(max_length=50,default=None)
    experience=models.CharField(max_length=500,default=None)
    job_expired_date=models.CharField(max_length=100,default=None)
    functional_area=models.CharField(max_length=100,default=None)
    salary_compensation=models.CharField(max_length=200,default=None)
    travel_requirement=models.CharField(max_length=100,default=None)
    employer=models.CharField(max_length=100,default=None)
    organization_type=models.CharField(max_length=100,default=None)
    company_type_relation=models.CharField(max_length=100,default=None)
    FLSA_status=models.CharField(max_length=100,default=None)
    job_roles_responsibilities=models.TextField(default=None)
    related_jobs=models.CharField(max_length=200,default=None)
    web_creative_services=models.CharField(max_length=100,default=None)
    job_questions=models.TextField(default=None)
    job_requirements=models.TextField(default=None)
    weekly_hours=models.CharField(max_length=10,default=None)
    opportunities=models.CharField(max_length=200,default=None)
    available_time=models.CharField(max_length=55,default=None)
    discipline=models.CharField(max_length=255,default=None)
    work_shift=models.CharField(max_length=200,default=None)
    relocation_available=models.CharField(max_length=50,default=None)
    ITAR=models.CharField(max_length=255,default=None)
    company_description=models.TextField(default=None)
    selection_process=models.CharField(max_length=100,default=None)
    employee_status=models.CharField(max_length=100,default=None)
    company_level=models.CharField(max_length=100,default=None)
    job_tracking_code=models.CharField(max_length=20,default=None)
    travel_allowance=models.CharField(max_length=55,default=None)
    skills_preferred=models.CharField(max_length=500,default=None)
    skills_required=models.TextField(default=None)
    employer_email=models.CharField(max_length=100,default=None)
    employer_contact=models.CharField(max_length=20,default=None)
    enquiry_details=models.CharField(max_length=200,default=None)
    important_notes=models.TextField(default=None)
    country_type=models.CharField(max_length=50,default=None)
    scrapped_date=models.DateTimeField(default=None)
    scrappedBy=models.CharField(max_length=50,default=None)
    deleted_status=models.TextField(default=None)
class company_info(models.Model):
    class Meta:
        db_table='company_info'
    company_info_id=models.IntegerField(primary_key=True)
    company_name=models.CharField(max_length=255)
    company_size=models.CharField(max_length=45)
    company_website=models.TextField()
    company_logo_path=models.TextField()
    company_contact=models.CharField(max_length=20)
    company_profile_description=models.TextField()
    image_purity=models.CharField(max_length=45)
    estd_year=models.CharField(max_length=20)
    other_locations=models.TextField(max_length=1000,default=None)
    hq_company_address_line1=models.TextField()
    hq_company_address_line2=models.CharField(max_length=255)
class companies_internship(models.Model):
    class Meta:
        db_table='companies_internship'
    company_info_company_info_id=models.IntegerField()
    companies_internship_id=models.IntegerField(primary_key=True)
    company_name=models.CharField(max_length=255)
    contact_city=models.CharField(max_length=55)
    contact_state_code=models.CharField(max_length=10)
    contact_address=models.CharField(max_length=255)
    contact_website=models.CharField(max_length=255)
    internship_name=models.CharField(max_length=255)
class StoreLocation(models.Model):
    class Meta:
        db_table='locations'
    location_id=models.IntegerField(primary_key=True)
    country_code=models.CharField(max_length=5)
    city=models.CharField(max_length=180)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    state_code=models.CharField(max_length=20)
    postal_code=models.CharField(max_length=20)

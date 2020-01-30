from django.db import models
class Bugs(models.Model):
    class Meta:
        db_table='Bugs'
        get_latest_by = 'Bug_id'
    Bug_id=models.IntegerField(primary_key=True)
    Resolved=models.CharField(max_length=50)
    Assigned_date=models.DateTimeField()
    Bug_description=models.TextField()
    Bug_assigned_by=models.CharField(max_length=50)
    Bug_assigned_to=models.CharField(max_length=50)
    company_info_id=models.IntegerField()
    ResolvedDate=models.DateTimeField()
class StoreLocation(models.Model):
    class Meta:
        db_table='locations'
    location_id=models.IntegerField(primary_key=True)
    country_code=models.CharField(max_length=5)
    city=models.CharField(max_length=180)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    state_code=models.CharField(max_length=20)
class Web_internships_jobs_forSerlize(models.Model):
    class Meta:
        db_table='web_internship_jobs'
    web_internship_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100)
    company_info_id=models.CharField(max_length=100)
    scrappedBy=models.CharField(max_length=50)
    job_title=models.CharField(max_length=255)
    job_description=models.TextField()
    company_name=models.CharField(max_length=255)
    job_location=models.TextField()
    experience_level=models.CharField(max_length=250)
    apply_link=models.TextField()
    posted_date=models.DateTimeField()
    qualifications=models.TextField()
    job_type=models.CharField(max_length=100)
    other_locations=models.CharField(max_length=1000)
    schedule_job_timings=models.CharField(max_length=100)
    industry_type=models.CharField(max_length=50)
    experience=models.CharField(max_length=500)
    job_expired_date=models.CharField(max_length=100)
    functional_area=models.CharField(max_length=100)
    salary_compensation=models.CharField(max_length=200)
    travel_requirement=models.CharField(max_length=100)
    employer=models.CharField(max_length=100)
    organization_type=models.CharField(max_length=100)
    company_type_relation=models.CharField(max_length=100)
    FLSA_status=models.CharField(max_length=100)
    job_roles_responsibilities=models.TextField()
    related_jobs=models.CharField(max_length=200)
    web_creative_services=models.CharField(max_length=100)
    job_questions=models.TextField()
    job_requirements=models.TextField()
    weekly_hours=models.CharField(max_length=10)
    opportunities=models.CharField(max_length=200)
    available_time=models.CharField(max_length=55)
    discipline=models.CharField(max_length=255)
    work_shift=models.CharField(max_length=200)
    relocation_available=models.CharField(max_length=50)
    ITAR=models.CharField(max_length=255)
    tested_status=models.CharField(max_length=50)
    company_description=models.TextField()
    selection_process=models.CharField(max_length=100)
    employee_status=models.CharField(max_length=100)
    company_level=models.CharField(max_length=100)
    job_tracking_code=models.CharField(max_length=20)
    travel_allowance=models.CharField(max_length=55)
    skills_preferred=models.CharField(max_length=500)
    skills_required=models.TextField()
    employer_email=models.CharField(max_length=100)
    employer_contact=models.CharField(max_length=20)
    enquiry_details=models.CharField(max_length=200)
    important_notes=models.TextField()
    country_type=models.CharField(max_length=50)
    scrapped_date=models.DateTimeField()
    scrapped_location=models.TextField()
    other_locations=models.TextField()
    dcount=models.CharField(max_length=50)
class Web_internships_jobs(models.Model):
    class Meta:
        db_table='web_internship_jobs'
    web_internship_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100)
    company_info_id=models.CharField(max_length=100)
    scrappedBy=models.CharField(max_length=50)
    job_title=models.CharField(max_length=255)
    job_description=models.TextField()
    company_name=models.CharField(max_length=255)
    job_location=models.TextField()
    experience_level=models.CharField(max_length=250)
    apply_link=models.TextField()
    posted_date=models.DateTimeField()
    qualifications=models.TextField()
    job_type=models.CharField(max_length=100)
    other_locations=models.CharField(max_length=1000)
    schedule_job_timings=models.CharField(max_length=100)
    industry_type=models.CharField(max_length=50)
    experience=models.CharField(max_length=500)
    job_expired_date=models.CharField(max_length=100)
    functional_area=models.CharField(max_length=100)
    salary_compensation=models.CharField(max_length=200)
    travel_requirement=models.CharField(max_length=100)
    employer=models.CharField(max_length=100)
    organization_type=models.CharField(max_length=100)
    company_type_relation=models.CharField(max_length=100)
    FLSA_status=models.CharField(max_length=100)
    job_roles_responsibilities=models.TextField()
    related_jobs=models.CharField(max_length=200)
    web_creative_services=models.CharField(max_length=100)
    job_questions=models.TextField()
    job_requirements=models.TextField()
    weekly_hours=models.CharField(max_length=10)
    opportunities=models.CharField(max_length=200)
    available_time=models.CharField(max_length=55)
    discipline=models.CharField(max_length=255)
    work_shift=models.CharField(max_length=200)
    relocation_available=models.CharField(max_length=50)
    ITAR=models.CharField(max_length=255)
    tested_status=models.CharField(max_length=50)
    company_description=models.TextField()
    selection_process=models.CharField(max_length=100)
    employee_status=models.CharField(max_length=100)
    company_level=models.CharField(max_length=100)
    job_tracking_code=models.CharField(max_length=20)
    travel_allowance=models.CharField(max_length=55)
    skills_preferred=models.CharField(max_length=500)
    skills_required=models.TextField()
    employer_email=models.CharField(max_length=100)
    employer_contact=models.CharField(max_length=20)
    enquiry_details=models.CharField(max_length=200)
    important_notes=models.TextField()
    country_type=models.CharField(max_length=50)
    scrapped_date=models.DateTimeField()
    scrapped_location=models.TextField()
    other_locations=models.TextField()


class Web_company_jobs(models.Model):
    class Meta:
        db_table='web_company_jobs'
    web_company_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100)
    company_info_id=models.CharField(max_length=100)
    job_title=models.CharField(max_length=255)
    tested_status=models.CharField(max_length=50)
    job_description=models.TextField()
    company_name=models.CharField(max_length=255)
    job_location=models.TextField()
    apply_link=models.TextField()
    scrappedBy = models.CharField(max_length=50)
    posted_date=models.DateTimeField()
    other_locations=models.CharField(max_length=1000)
    qualifications=models.TextField()
    job_type=models.CharField(max_length=100)
    schedule_job_timings=models.CharField(max_length=100)
    industry_type=models.CharField(max_length=50)
    experience=models.CharField(max_length=500)
    experience_level=models.CharField(max_length=250)
    job_expired_date=models.CharField(max_length=100)
    functional_area=models.CharField(max_length=100)
    salary_compensation=models.CharField(max_length=200)
    travel_requirement=models.CharField(max_length=100)
    employer=models.CharField(max_length=100)
    organization_type=models.CharField(max_length=100)
    company_type_relation=models.CharField(max_length=100)
    FLSA_status=models.CharField(max_length=100)
    job_roles_responsibilities=models.TextField()
    related_jobs=models.CharField(max_length=200)
    web_creative_services=models.CharField(max_length=100)
    job_questions=models.TextField()
    job_requirements=models.TextField()
    weekly_hours=models.CharField(max_length=10)
    opportunities=models.CharField(max_length=200)
    available_time=models.CharField(max_length=55)
    discipline=models.CharField(max_length=255)
    work_shift=models.CharField(max_length=200)
    relocation_available=models.CharField(max_length=50)
    ITAR=models.CharField(max_length=255)
    company_description=models.TextField()
    selection_process=models.CharField(max_length=100)
    employee_status=models.CharField(max_length=100)
    company_level=models.CharField(max_length=100)
    job_tracking_code=models.CharField(max_length=20)
    travel_allowance=models.CharField(max_length=55)
    skills_preferred=models.CharField(max_length=500)
    skills_required=models.TextField()
    employer_email=models.CharField(max_length=100)
    employer_contact=models.CharField(max_length=20)
    enquiry_details=models.CharField(max_length=200)
    important_notes=models.TextField()
    country_type=models.CharField(max_length=50)
    scrapped_location=models.TextField()
    scrapped_date=models.DateTimeField()
class Web_company_jobs_forSerlize(models.Model):
    class Meta:
        db_table='web_company_jobs'
    dcount=models.CharField(max_length=50)
    web_company_jobs_id=models.BigIntegerField(primary_key=True)
    job_id=models.CharField(max_length=100)
    company_info_id=models.CharField(max_length=100)
    job_title=models.CharField(max_length=255)
    tested_status=models.CharField(max_length=50)
    job_description=models.TextField()
    company_name=models.CharField(max_length=255)
    job_location=models.TextField()
    apply_link=models.TextField()
    scrappedBy = models.CharField(max_length=50)
    posted_date=models.DateTimeField()
    other_locations=models.CharField(max_length=1000)
    qualifications=models.TextField()
    job_type=models.CharField(max_length=100)
    schedule_job_timings=models.CharField(max_length=100)
    industry_type=models.CharField(max_length=50)
    experience=models.CharField(max_length=500)
    experience_level=models.CharField(max_length=250)
    job_expired_date=models.CharField(max_length=100)
    functional_area=models.CharField(max_length=100)
    salary_compensation=models.CharField(max_length=200)
    travel_requirement=models.CharField(max_length=100)
    employer=models.CharField(max_length=100)
    organization_type=models.CharField(max_length=100)
    company_type_relation=models.CharField(max_length=100)
    FLSA_status=models.CharField(max_length=100)
    job_roles_responsibilities=models.TextField()
    related_jobs=models.CharField(max_length=200)
    web_creative_services=models.CharField(max_length=100)
    job_questions=models.TextField()
    job_requirements=models.TextField()
    weekly_hours=models.CharField(max_length=10)
    opportunities=models.CharField(max_length=200)
    available_time=models.CharField(max_length=55)
    discipline=models.CharField(max_length=255)
    work_shift=models.CharField(max_length=200)
    relocation_available=models.CharField(max_length=50)
    ITAR=models.CharField(max_length=255)
    company_description=models.TextField()
    selection_process=models.CharField(max_length=100)
    employee_status=models.CharField(max_length=100)
    company_level=models.CharField(max_length=100)
    job_tracking_code=models.CharField(max_length=20)
    travel_allowance=models.CharField(max_length=55)
    skills_preferred=models.CharField(max_length=500)
    skills_required=models.TextField()
    employer_email=models.CharField(max_length=100)
    employer_contact=models.CharField(max_length=20)
    enquiry_details=models.CharField(max_length=200)
    important_notes=models.TextField()
    country_type=models.CharField(max_length=50)
    scrapped_location=models.TextField()
    scrapped_date=models.DateTimeField()
class company_info(models.Model):
    class Meta:
        get_latest_by = 'company_info_id'
        db_table='company_info'
    company_info_id=models.IntegerField(primary_key=True,)
    company_name=models.CharField(max_length=255)
    company_size=models.CharField(max_length=45,default=None)
    company_website=models.TextField(default=None)
    company_logo_path=models.TextField(default=None)
    company_contact=models.CharField(max_length=20,default=None)
    company_profile_description=models.TextField(default=None)
    image_purity=models.CharField(max_length=45,default=None)
    estd_year=models.CharField(max_length=20,default=None)
    other_locations=models.TextField(default=None)
    hq_company_address_line1=models.TextField(default=None)
    hq_company_address_line2=models.CharField(max_length=255,default=None)
    company_unique_id=models.CharField(max_length=50,default=None)


class company_infoCopy(models.Model):
    class Meta:
        db_table='company_info'
        get_latest_by='company_info_id'
    company_info_id=models.IntegerField(primary_key=True,)
    company_name=models.CharField(max_length=255)
    company_size=models.CharField(max_length=45)
    company_website=models.TextField()
    hq_locations_location_id=models.IntegerField()
    company_logo_path=models.TextField()
    company_contact=models.CharField(max_length=20)
    company_profile_description=models.TextField()
    image_purity=models.CharField(max_length=45)
    estd_year=models.CharField(max_length=20)
    company_unique_id=models.CharField(max_length=10)
    hq_company_address_line1=models.TextField()
    hq_company_address_line2=models.CharField(max_length=255)
class Locations(models.Model):
    class Meta:
        db_table='locations'
    location_id=models.IntegerField(primary_key=True)
    country_code=models.CharField(max_length=5)
    postal_code=models.CharField(max_length=20)
    city=models.CharField(max_length=180)
    state=models.CharField(max_length=100)
    state_code=models.CharField(max_length=20)
    postal_code=models.CharField(max_length=20)

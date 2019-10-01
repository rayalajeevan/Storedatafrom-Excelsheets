
from django.db import models


class WebCompanyJobs(models.Model):
    web_company_jobs_id = models.BigAutoField(primary_key=True)
    company_info_id = models.CharField(max_length=100, blank=True, null=True)
    job_id = models.CharField(max_length=1000, blank=True, null=True)
    job_title = models.CharField(max_length=1000, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    job_location = models.TextField(blank=True, null=True)
    apply_link = models.TextField(blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    deleted_status = models.CharField(max_length=10, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    job_type = models.TextField(blank=True, null=True)
    schedule_job_timings = models.CharField(max_length=500, blank=True, null=True)
    industry_type = models.CharField(max_length=500, blank=True, null=True)
    experience = models.CharField(max_length=500, blank=True, null=True)
    job_expired_date = models.CharField(max_length=300, blank=True, null=True)
    functional_area = models.CharField(max_length=800, blank=True, null=True)
    salary_compensation = models.CharField(max_length=500, blank=True, null=True)
    travel_requirement = models.CharField(max_length=1000, blank=True, null=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    organization_type = models.CharField(max_length=1000, blank=True, null=True)
    company_type_relation = models.CharField(max_length=100, blank=True, null=True)
    flsa_status = models.CharField(db_column='FLSA_status', max_length=600, blank=True, null=True)  # Field name made lowercase.
    job_roles_responsibilities = models.TextField(blank=True, null=True)
    related_jobs = models.CharField(max_length=200, blank=True, null=True)
    job_questions = models.TextField(blank=True, null=True)
    job_requirements = models.TextField(blank=True, null=True)
    weekly_hours = models.CharField(max_length=200, blank=True, null=True)
    opportunities = models.CharField(max_length=200, blank=True, null=True)
    employee_status = models.CharField(max_length=1000, blank=True, null=True)
    web_creative_services = models.CharField(max_length=100, blank=True, null=True)
    available_time = models.CharField(max_length=55, blank=True, null=True)
    discipline = models.TextField(blank=True, null=True)
    work_shift = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    relocation_available = models.CharField(max_length=300, blank=True, null=True)
    itar = models.CharField(db_column='ITAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company_description = models.TextField(blank=True, null=True)
    selection_process = models.CharField(max_length=100, blank=True, null=True)
    job_services = models.TextField(blank=True, null=True)
    company_level = models.CharField(max_length=100, blank=True, null=True)
    job_tracking_code = models.CharField(max_length=20, blank=True, null=True)
    travel_allowance = models.CharField(max_length=55, blank=True, null=True)
    skills_preferred = models.TextField(blank=True, null=True)
    skills_required = models.TextField(blank=True, null=True)
    employer_email = models.CharField(max_length=100, blank=True, null=True)
    employer_contact = models.CharField(max_length=20, blank=True, null=True)
    enquiry_details = models.CharField(max_length=200, blank=True, null=True)
    important_notes = models.TextField(blank=True, null=True)
    country_type = models.CharField(max_length=50, blank=True, null=True)
    scrapped_date = models.DateTimeField(blank=True, null=True)
    scrappedby = models.CharField(db_column='scrappedBy',max_length=50)
    other_locations = models.CharField(max_length=1000, blank=True, null=True)
    scrapped_location = models.TextField(blank=True, null=True)
    tested_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_company_jobs'


class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=180, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    state_code = models.CharField(max_length=20, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    county_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    accuracy = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    location_type = models.CharField(max_length=15, blank=True, null=True)
    street_area = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'
class BeautifyCompanyJobs(models.Model):
    beautify_company_id = models.AutoField(primary_key=True)
    company_info_id = models.IntegerField()
    instruction_id = models.IntegerField()
    html_tags=models.CharField(max_length=250)
    keywords=models.CharField(max_length=250)
    attrs=models.CharField(max_length=250)
    apply_link=models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'beautify_company_jobs'


class WebInternshipJobs(models.Model):
    web_internship_jobs_id = models.BigAutoField(primary_key=True)
    job_id = models.CharField(max_length=1000, blank=True, null=True)
    company_id = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=1000, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    job_location = models.TextField(blank=True, null=True)
    apply_link = models.TextField(blank=True, null=True)
    posted_date = models.DateTimeField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    deleted_status = models.CharField(max_length=10, blank=True, null=True)
    job_type = models.TextField(blank=True, null=True)
    schedule_job_timings = models.CharField(max_length=500, blank=True, null=True)
    industry_type = models.CharField(max_length=500, blank=True, null=True)
    experience = models.CharField(max_length=500, blank=True, null=True)
    job_expired_date = models.CharField(max_length=300, blank=True, null=True)
    functional_area = models.CharField(max_length=500, blank=True, null=True)
    salary_compensation = models.CharField(max_length=500, blank=True, null=True)
    travel_requirement = models.CharField(max_length=1000, blank=True, null=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    organization_type = models.CharField(max_length=1000, blank=True, null=True)
    company_type_relation = models.CharField(max_length=100, blank=True, null=True)
    flsa_status = models.CharField(db_column='FLSA_status', max_length=600, blank=True, null=True)  # Field name made lowercase.
    job_roles_responsibilities = models.TextField(blank=True, null=True)
    related_jobs = models.CharField(max_length=200, blank=True, null=True)
    job_questions = models.TextField(blank=True, null=True)
    job_requirements = models.TextField(blank=True, null=True)
    weekly_hours = models.CharField(max_length=200, blank=True, null=True)
    job_services = models.TextField(blank=True, null=True)
    opportunities = models.CharField(max_length=200, blank=True, null=True)
    web_creative_services = models.CharField(max_length=100, blank=True, null=True)
    employee_status = models.CharField(max_length=1000, blank=True, null=True)
    available_time = models.CharField(max_length=55, blank=True, null=True)
    discipline = models.TextField(blank=True, null=True)
    work_shift = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    relocation_available = models.CharField(max_length=300, blank=True, null=True)
    itar = models.CharField(db_column='ITAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    company_description = models.TextField(blank=True, null=True)
    selection_process = models.CharField(max_length=100, blank=True, null=True)
    company_level = models.CharField(max_length=100, blank=True, null=True)
    job_tracking_code = models.CharField(max_length=20, blank=True, null=True)
    travel_allowance = models.CharField(max_length=55, blank=True, null=True)
    skills_preferred = models.TextField(blank=True, null=True)
    skills_required = models.TextField(blank=True, null=True)
    employer_email = models.CharField(max_length=100, blank=True, null=True)
    employer_contact = models.CharField(max_length=20, blank=True, null=True)
    enquiry_details = models.CharField(max_length=200, blank=True, null=True)
    important_notes = models.TextField(blank=True, null=True)
    country_type = models.CharField(max_length=50, blank=True, null=True)
    scrapped_date = models.DateTimeField(blank=True, null=True)
    internship_id = models.BigIntegerField(blank=True, null=True)
    scrappedby = models.CharField(db_column='scrappedBy', max_length=50, blank=True, null=True)  # Field namemade lowercase.
    other_locations = models.CharField(max_length=1000, blank=True, null=True)
    company_info_id = models.BigIntegerField(blank=True, null=True)
    tested_status = models.CharField(max_length=50, blank=True, null=True)
    scrapped_location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_internship_jobs'
class TopCities(models.Model):
    top_cities_id = models.BigAutoField(primary_key=True)
    city_name = models.CharField(max_length=45, blank=True, null=True)
    state_code = models.CharField(max_length=5, blank=True, null=True)
    country_type = models.CharField(max_length=45, blank=True, null=True)
    top_cities_type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'top_cities'
if __name__=="__main__":
    print("hello")

from django.db import models

# Create your models here.
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
        app_label='web_scrapping'
class CompanyInfo(models.Model):
    company_info_id = models.BigAutoField(primary_key=True)
    company_size = models.CharField(max_length=45, blank=True, null=True)
    company_website = models.TextField(blank=True, null=True)
    company_name = models.CharField(unique=True, max_length=255)
    company_logo_path = models.TextField(blank=True, null=True)
    company_contact = models.CharField(max_length=20, blank=True, null=True)
    company_profile_description = models.TextField(blank=True, null=True)
    image_purity = models.CharField(max_length=45, blank=True, null=True)
    estd_year = models.CharField(max_length=20, blank=True, null=True)
    hq_locations_location = models.ForeignKey('Locations', models.DO_NOTHING, blank=True, null=True)
    hq_company_address_line1 = models.TextField(blank=True, null=True)
    hq_company_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    # industries_industry = models.ForeignKey('Industries', models.DO_NOTHING, blank=True, null=True)
    is_e_verify = models.CharField(max_length=45, blank=True, null=True)
    is_claimed = models.IntegerField(blank=True, null=True)
    fortune_rank = models.IntegerField(blank=True, null=True)
    is_flat_file_company = models.IntegerField(blank=True, null=True)
    is_company_verified = models.IntegerField(blank=True, null=True)
    hq_phone = models.CharField(max_length=15, blank=True, null=True)
    hq_phone_ext = models.CharField(max_length=10, blank=True, null=True)
    hq_fax = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=250, blank=True, null=True)
    industry = models.CharField(max_length=250, blank=True, null=True)
    sic = models.CharField(max_length=1500, blank=True, null=True)
    naics = models.CharField(max_length=1000, blank=True, null=True)
    all_employees = models.CharField(max_length=10, blank=True, null=True)
    total_company_locations = models.CharField(max_length=10, blank=True, null=True)
    company_priority_number = models.BigIntegerField(blank=True, null=True)
    country_type = models.CharField(max_length=10, blank=True, null=True)
    company_unique_id = models.CharField(max_length=10, blank=True, null=True)
    sudo_company_name = models.CharField(max_length=255, blank=True, null=True)
    redirect_url = models.CharField(max_length=1000, blank=True, null=True)
    company_cover_pic = models.TextField(blank=True, null=True)
    comp_cover_pic_profaniity = models.TextField(blank=True, null=True)
    sized_company = models.CharField(max_length=20, blank=True, null=True)
    uppers = models.TextField(blank=True, null=True)
    downers = models.TextField(blank=True, null=True)
    bottom_line = models.TextField(blank=True, null=True)
    employer_type = models.CharField(max_length=100, blank=True, null=True)
    stock_exchange = models.CharField(max_length=100, blank=True, null=True)
    president_and_ceo = models.CharField(max_length=500, blank=True, null=True)
    chairman = models.CharField(max_length=500, blank=True, null=True)
    no_of_employees_at_year = models.IntegerField(blank=True, null=True)
    ceo = models.CharField(max_length=100, blank=True, null=True)
    vice_chairman = models.CharField(max_length=100, blank=True, null=True)
    chairman_and_ceo = models.CharField(max_length=100, blank=True, null=True)
    vice_president_operations = models.CharField(max_length=500, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    company_stats = models.TextField(blank=True, null=True)
    stock_symbol = models.CharField(max_length=100, blank=True, null=True)
    other_locations = models.TextField(blank=True, null=True)
    engineer = models.CharField(max_length=100, blank=True, null=True)
    company_category = models.CharField(max_length=50, blank=True, null=True)
    es_status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info'
        app_label='web_scrapping'


# class CompanyIndustries(models.Model):
#     company_industries_id = models.BigAutoField(primary_key=True)
#     company_info = models.ForeignKey('CompanyInfo', models.DO_NOTHING, blank=True, null=True)
#     industry = models.ForeignKey('Industries', models.DO_NOTHING, blank=True, null=True)
#     industry_type = models.CharField(max_length=10)
#
#     class Meta:
#         managed = False
#         db_table = 'company_industries'
#         app_label='pushcompany'
class Industries(models.Model):
    industry_id = models.AutoField(primary_key=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    group_codes = models.CharField(max_length=20, blank=True, null=True)
    industry_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'industries'
        app_label='pushcompany'

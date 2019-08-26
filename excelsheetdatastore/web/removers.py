import datetime
import re
def dataModify(job_location,company_info_id,job_title,apply_link,company_name,job_description=None,job_id=None,job_type=None,posted_date=None,job_expired_date=None,qualifications=None,schedule_job_timings=None,industry_type=None,experience=None,functional_area=None,salary_compensation=None,travel_requirement=None,employer=None,organization_type=None,related_company=None,flsa_status=None,job_roles_responsibilities="",related_jobs=None,web_creative_services=None,job_questions=None,job_requirements=None,weekly_hours=None,job_services=None,opportunities=None,available_time=None,discipline=None,work_shift=None,relocation_available=None,itar=None,company_description=None,selection_process=None,employee_status=None,travel_allowance=None,skills_preferred=None,skills_required=None,email=None,enquiry_details=None,important_note=None,company_level=None,job_tracking_code=None,employer_contact=None,company_id=None,job_description1='',job_description2='',file_name=None,travel_required=None,travel_allowances=None,web_scrapping_main_id=0,company_type_relation=None,employer_email=None,job_id1=None,job_id2=None,country=None,other_locations=None,scrapped_location=None):

    return None
def regulardate(date=None):
    date=date.strip()
    try:
        value=re.search('\d+',date).group()
    except:
        value=None
    if value==None:
        if 'day ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=1)
        elif 'week ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(weeks=1)
        elif 'month ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=30)
        elif 'year ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=365)
        elif 'minute ' in date.lower() or 'mins' in date.lower() or 'min' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(minutes=1)
        elif 'hour ' in date.lower() or 'hrs' in date.lower() or 'hr' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(hours=1)
        elif 'second ' in date.lower() or 'secs' in date.lower() or 'sec' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(seconds=1)
    else:
        if 'days' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'day' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'weeks' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(weeks=int(value))
        elif 'months' in date.lower():
            value=int(value)*30
            date=datetime.datetime.now()-datetime.timedelta(days=value)
        elif 'years' in date.lower():
            value=int(value)*365
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'minutes' in date.lower() or 'mins' in date.lower() or 'min' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(minutes=int(value))
        elif 'hours' in date.lower() or 'hrs' in date.lower() or 'hr' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(hours=int(value))
        elif 'week ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(weeks=int(value))
        elif 'month ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'year ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'minute ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(minutes=int(value))
        elif 'hour ' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(hours=int(value))
        elif 'second ' in date.lower() or 'secs' in date.lower() or 'sec' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(seconds=int(value))
        elif 'seconds' in date.lower():
            date=datetime.datetime.now()-datetime.timedelta(seconds=int(value))
    return date
from dateutil import parser
def validatos(date,*args,**kwrgs):
    datestr=None
    if  date!=None and date!=float('nan') and date!="" and date!='NULL' and date !="null" and date.strip()!="Not Specified" :
        date=date.strip()
        if 'yesterday' in date.lower():
            datestr=datetime.datetime.now()-datetime.timedelta(days=1)
            return datestr
        if 'today' in date.lower():
            return datetime.datetime.today().date()
        if 'week' in date.lower() or 'day' in date.lower() or 'year' in date.lower() or 'minutes' in date.lower() or 'hour' in date.lower() or 'month' in date.lower() or 'hr' in date.lower() or 'min' in date.lower() or 'sec' in date.lower():
            datestr=regulardate(str(date))
            return str(datestr)
        elif 'posted now' in date.lower() or 'few hours' in date.lower():
            return datetime.datetime.today().date()
        else:
            datestr=parser.parse(str(date))
            return str(datestr)
        if datestr==None:
            return datetime.datetime.today().date()
    else:
        return datetime.datetime.today().date()

import unicodedata
from  bs4 import BeautifulSoup
def string_error(data,*args,**kwrgs):
    if data!='' or data!='NULL' or data!='null' or data!=None or data!="None":
        try:
           unicode=unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode("utf-8")
           return unicodes
        except:
           return unicode
    else:
        return None

def replacer(data):
    data=data.replace('Job Description :','')
    data=data.replace('Job Description:','')
    data=data.replace('Job Description','')
    data=data.replace('Description:','')
    data=data.replace('Description','')
    return data
if __name__=="__main__":
    print(validatos("2019-02-14 13:27:07.5776992Z"))

import datetime
import re
import unicodedata
from bs4 import BeautifulSoup
from dateutil import parser
from copy import deepcopy
from fuzzywuzzy import fuzz
import time
import requests
from StoreJobsRestservice.models import Locations,BeautifyCompanyJobs
from langdetect import detect,detect_langs
from StoreJobsRestservice.instructions import Instructions
def locationIdentifier(org_location):
    job_location=None
    country_type=None
    location=deepcopy(org_location.strip().replace('#','').replace('&',''))
    location=location.replace(',','>').replace(';','>')
    locationSpliter=[x.strip() for x in location.split('>') if x.strip() !='']
    if len(locationSpliter)!=1:
        orginal_location=get_location_from_database(locationSpliter)
        if orginal_location.get('location')==0:
            orginal_location=get_location_from_googleApi(org_location)
    else:
        orginal_location=get_location_from_googleApi(org_location)
    if orginal_location.get('location')!=0:
        city=orginal_location.get('location').get('city')
        state=orginal_location.get('location').get('state_code')
        country_type=orginal_location.get('location').get('country_type')
        if city==None or state==None or country_type==None:
            job_location=org_location
            country_type=None
        else:
            try:
                state=int(state)
                state=country_type
                job_location=city+", "+state
            except:
                job_location=city+", "+state
    else:
        job_location=org_location
        country_type=None
    return {'job_location':job_location,'country_type':country_type,'scrapped_location':org_location}
def get_location_from_database(location):
    """
    get_location_from_database
     this function will search matched location in databases
     if matched
            returns matached city and state in dictionary
    if not
            it will call get_location_from_googleApi
    """
    city=None
    state=None
    country_type=None
    for index in location:
        if state!=None and city!=None:
            break
        if len(index)==2:
            state_data=Locations.objects.filter(state_code=index)
            if len(state_data)!=0:
                state=state_data[0].state_code
                continue
        if city==None:
            city_data=Locations.objects.filter(city=index)
            if len(city_data)!=0:
                city=city_data[0].city
                continue
        if state==None:
            state_data=Locations.objects.filter(state=index)
            if len(state_data)!=0:
                state=state_data[0].state_code
                continue
            if len(state_data)==0:
                state_data=Locations.objects.filter(state=index)
                if len(state_data)!=0:
                    state=state_data[0].state_code
                    continue
    if city==None or state==None:
        return {'location':0}
    if city!=None and state!=None:
        country_type=Locations.objects.filter(state_code=state,city=city)
        if len(country_type)!=0:
            country_type=country_type[0].country_code
            return {"location":{'city':city,'state_code':state,'country_type':country_type}}
        return {'location':0}
    return {'location':0}

def get_location_from_googleApi(location):
    """
    get_location_from_googleApi
     this function get the matched loaction from google api
        it will get 1 st loction from google API and checks with scrapped location
        if its matched
            returns city and state_code
        if not
            its calls the function checking_mateched_location
    """
    city=None
    state_code=None
    country_type=None
    try:
        location_request=requests.get('http://api.geonames.org/searchJSON?q={location}&maxRows=20&username=optncpt'.format(location=location.replace('#','')))
    except Exception as e:
        print("get_location_from_googleApi got Error So Sleeping for 20 secs")
        time.sleep(20)
        print(str(e))
        return get_location_from_googleApi(location)
    if location_request.status_code==200:
        location_data=location_request.json()
        try:
            if location_data.get('totalResultsCount')!=0 or location_data.get('totalResultsCount')!=None:
                if len(location_data['geonames'])!=0:
                    state_code=location_data['geonames'][0].get('adminCode1')
                    city=location_data['geonames'][0].get('name')
                    if city=='Bengaluru':
                        city='Bangalore'
                    country_type=location_data['geonames'][0].get('countryCode')
                    print("scrapped",location)
                    if fuzz.ratio(city.lower(), location.lower())>=55:
                        print('goog',{"location":{'city':city,'state_code':state_code,'country_type':country_type}})
                        return {"location":{'city':city,'state_code':state_code,'country_type':country_type}}
                    else:
                        print(checking_mateched_location(location,location_data))
                        return checking_mateched_location(location,location_data)
                else:
                    return {'location':0}
            else:
                return {'location':0}
        except:
            print("get_location_from_googleApi got error so sleeping 20 secs")
            time.sleep(20)
            return get_location_from_googleApi(location)
    else:
        print("get_location_from_googleApi not got 200 status So Sleeping for 20 secs")
        time.sleep(20)
        return get_location_from_googleApi(location)
def checking_mateched_location(scrapped_location,google_location):
    """
    checking_mateched_location
    it will check all locations which locations given google API and checks with scrapped location
        if its matched
            returns city and state_code
        if not
            returns 0

    """
    for g_loc in google_location['geonames']:
        if g_loc['name'].lower() in scrapped_location.lower():
            state_code=g_loc.get('adminCode1')
            city= g_loc.get('name')
            country_type= g_loc.get('countryCode')
            return {"location":{'city':city,'state_code':state_code,'country_type':country_type}}
        else:
            for x in scrapped_location.split(' '):
                if x.strip()!='' and len(x)>4 and fuzz.ratio(x.lower(), g_loc['name'].lower())>=55:
                    state_code=g_loc.get('adminCode1')
                    city= g_loc.get('name')
                    country_type= g_loc.get('countryCode')
                    return {"location":{'city':city,'state_code':state_code,'country_type':country_type}}
    return  {'location':0}
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

def validatos(date,*args,**kwrgs):
    datestr=None
    if  date!=None and date!=float('nan') and date!="" and date!='NULL' and date !="null" and date.strip()!="Not Specified" :
        date=date.strip()
        if 'yesterday' in date.lower():
            datestr=datetime.datetime.now()-datetime.timedelta(days=1)
            return datestr
        if 'today' in date.lower():
            return datetime.datetime.now()
        if 'week' in date.lower() or 'day' in date.lower() or 'year' in date.lower() or 'minutes' in date.lower() or 'hour' in date.lower() or 'month' in date.lower() or 'hr' in date.lower() or 'min' in date.lower() or 'sec' in date.lower():
            datestr=regulardate(str(date))
            return str(datestr)
        elif 'posted now' in date.lower() or 'few hours' in date.lower():
            return datetime.datetime.now()
        else:
            try:
                datestr=parser.parse(str(date))
                return str(datestr)
            except Exception as exc:
                print(exc)
                return str(datetime.datetime.now())
        if datestr==None:
            return str(datetime.datetime.now())
    else:
        return str(datetime.datetime.now())



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
def HtmlParser(data,job):
    soup=BeautifulSoup(data,"html.parser")
    datarefineer=['primary_location',
                'recruiter_name',
                'job_id']
    datarefineer_identifier=['class','id','name']
    for x in datarefineer_identifier:
        for y in datarefineer:
            for refine in soup.findAll({x:y}):
                refine.decompose()
    for x in soup.findAll('a'):
        if 'http' in x.get_text().strip().lower() or 'www.' in x.get_text().strip().lower() or '.org' in x.get_text().strip().lower() or '.in' in x.get_text().strip().lower() or '.com' in x.get_text().strip().lower():
            x.decompose()
            continue
        x.attrs=None
    RemovableTags=['button','submit','img','script','path','svg','input','hr','select','iframe','textarea']
    for tag in RemovableTags:
        for x in soup.findAll(tag):
            x.decompose()
    REMOVE_ATTRIBUTES = [
    'lang','language','onmouseover','onmouseout','script','font',
    'dir','face','color','hspace',
    'border','valign','align','background','bgcolor','link','vlink',
    'alink','href','id','src','type','border','align']
    soup = BeautifulSoup(str(soup),"html.parser")
    for attr in REMOVE_ATTRIBUTES:
        for tag in soup.findAll():
            	del tag[attr]
    for x in [soup.find('div',{'video-container small-video centerOrient':'true'}),soup.find('div',{'class':'iCIMS_JobOptions'}),soup.find('div',{'class':'iCIMS_JobHeaderGroup'})]:
        if x!=None:
            x.decompose()
    for x in soup.findAll():
         if len(x.findChildren())==0:
            if '#' in x.getText().strip() and len(x.getText().strip())<=20:
                x.decompose()
                break
            if '*' in x.getText().strip() and  len(x.getText().strip())<=20:
                 x.decompose()
                 break
    removed_elements=[]
    for x in soup.findAll():
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_title','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_location','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('functional_area','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_id','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_type','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('work_shift','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_title','qwertyuiopasdfghjklzxcvbnm').lower()+" "+job.get('job_location','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            continue
            if x.parent!=None and len(x.parent.get_text().strip())<=200:
                x.parent.decompose()
            else:
                if len(x.get_text().strip())<=100:
                    x.decompose()
        if 'job title::' in x.getText().strip().lower():
            if x.name=='strong':
                if 'location:' in x.parent().getText().strip():
                    x.parent.decompose()
        if 'Job ID:' in  x.get_text().strip():
            if x.parent!=None and len(x.parent.get_text().strip())<=45:
                x.parent.decompose()
            else:
                if len(x.get_text().strip())<=50:
                    x.decompose()
        for item in ['Deadline','Salary','Deadline:','Salary:','location:','locations:','work location(s):','team:', 'reports to:','title:','hours:','pay rate:','Req. ID:','Recruiter:','Role:','Position Location:','Reports To:','Allocation Specialist','Business Unit:','Supervision:','Supervision:','Full Time, Fixed Term - 12 Months','Requisition ID:','Position Title:','Project:','Relocation Authorized:','Position to be Panel Interviewed?','Grade:','Work Authorization:','Other Requirements:','Company:','Req ID:','Date:','Start Date:','Work type:','Categories:','Job no:','Contract:','Profile :','Scope :','POSITION:','DEPARTMENT:','BASE RATE OF PAY:','SHIFT:','Your future manager :','Scope :','Reporting Relationship','Employee Status:','Work Location:','Role Location:','Role Type:','Shift Schedule:','Rostered Hours:','Hours and shift type']:
           if item.strip() in x.getText().strip():
                if x.parent!=None and len(x.parent.get_text().strip())<=70:
                    removed_elements.append(str(x.parent))
                    x.parent.decompose()
                else:
                    if len(x.get_text().strip())<=100:
                        removed_elements.append(str(x))
                        x.decompose()
    for ele in removed_elements:
        soup=str(soup)+str(ele)
    soup=str(soup).replace('&#8203','').replace('Duties: JOB DESCRIPTION','')
    return replacer(str(soup))
def refineColumns(job):
    new_jobData={}
    for key,value in job.items():
        if value!=None:
            if 'job_description'in key.lower():
                if 'job_description' !=key.lower():
                    new_jobData['job_description']=string_error(new_jobData.get('job_description')+value)
                    continue
                else:
                    if new_jobData.get('job_description')==None:
                        new_jobData['job_description']=string_error(job.get('job_description'))
                        continue
            elif 'qualifications'in key.lower():
                if 'qualifications' !=key.lower():
                    new_jobData['qualifications']=string_error(new_jobData.get('qualifications')+value)
                    continue
                else:
                    if new_jobData.get('qualifications')==None:
                        new_jobData['qualifications']=string_error(job.get('qualifications'))
                        continue
            elif 'job_roles_responsibilities'in key.lower():
                if 'job_roles_responsibilities' !=key.lower():
                    new_jobData['job_roles_responsibilities']=string_error(new_jobData.get('job_roles_responsibilities')+value)
                    continue
                else:
                    if new_jobData.get('job_roles_responsibilities')==None:
                        new_jobData['job_roles_responsibilities']=string_error(job.get('job_roles_responsibilities'))
                        continue
            else:
                if 'flsa_status'==key:
                    new_jobData["FLSA_status"]=string_error(value)
                    continue
                if 'itar'==key:
                    new_jobData["ITAR"]=string_error(value)
                    continue
                new_jobData[key.lower()]=string_error(value)
    return new_jobData
def refining_job(job):
    # removing Null values
    job_data={}
    for job_key,job_value in job.items():
        if job_value!=None and str(job_value).strip().lower()!='null' and str(job_value).strip()!='':
            job_data[job_key]=job_value
    job=job_data

    job=dict([(k.lower(),str(v).strip()) for k,v in job.items() ])#converting keys to lowercase

    #refineColumns
    job=refineColumns(job)
    #get location with postal_code
    pin=None
    if job.get('pin')!=None:
        data=Locations.objects.filter(postal_code=job.get('pin'))
        if len(data)!=0:
            job['job_location']=data[0].city+", "+data[0].state_code
            job['country_type']=data[0].country_code
            pin="modified"
            del job['pin']
    #validateing column names

    for column_name in ['job_title','company_info_id','company_name','job_location','apply_link']:
        if job.get(column_name)==None:
            return {'error':{'column_name_error':'{} column name is missing'.format(column_name)}}
        elif job.get(column_name)=='':
            return {'error':{'column_data_error':'{} column name exist but data is missing'.format(column_name)}}
    if job.get('job_description')==None and job.get('job_roles_responsibilities')==None and job.get('qualifications')==None and job.get('job_requirements')==None:
        return {'error':{'column_name_error':"['job_description','job_roles_responsibilities','qualifications','job_requirements'] atleast one of the column must exist "}}

    #setting up city and state into location

    if job.get('job_location')==None:
        for column_name in ['city','state','country']:
            if job.get(column_name)!=None:
                if job.get('job_location')==None:
                    job['job_location']=job.get(column_name)
                else:
                    job['job_location']=job['job_location']+" "+job.get(column_name)
                del job[column_name]
    #setting the posted date in database information

    job['posted_date']=str(validatos(job.get('posted_date')))

    # detetcting JOB_TYPE
    job_type_list=['intern','part-time','full-time','part time','full time','regular','permanent','contract','half-time','half time','parttime','fulltime']
    for type in job_type_list:
        if job.get('job_type','@a1>2<').lower().strip() in type:
            job['job_type']=type.capitalize()
    #error throughing when postion was closed

    if 'position has been closed' in str(job.get('job_description')).lower():
        return {'error':{'position was closed':'Postion has been closed '}}

    #Beautify the Data-->removing unwanted data from particular company

    Beautify_objects=BeautifyCompanyJobs.objects.filter(company_info_id=job['company_info_id'])
    if len(Beautify_objects)!=0:
        for obj in Beautify_objects:
            job =Instructions(obj.instruction_id,job).method_caller()

    #identifying the internship or jobs
    type=None
    for value in [job['job_title'],job.get('job_type'),job.get('functional_area')]:
        value=str(value).strip()
        for identifiers in ['intern','intern.','intern,','intern ','internship','internship.','internship,','internship ','fellowship','fellowship.','fellowship,','fellowship ','aperentship','aperentship.','aperentship,','aperentship ','trainee','trainee.','trainee,','trainee ','apprenticeship','apprenticeship.','apprenticeship,','apprenticeship ']:
            if identifiers in [str(x).lower().strip() for x in value.split()]:
                type="INI"
    if type==None:
        type='JOB'

    #identifying the another languages job_description
    for item in ['Please refer to the corresponding language to initiate your application.','This job posting is only available in German language','This job posting is only available in German language','Sorry, this position has been filled']:
        if str(item).lower().strip() in str(job.get('job_description')).lower().strip():
            return {'error':{'another_language_job':'This job posting is only available in the language of the country where the position is located. Please refer to the corresponding language to initiate your application.'}}
    try:
        for x in ['job_description','job_roles_responsibilities','qualifications']:
            if str(job.get(x))!="None":
                job[x]=re.sub('\s+',' ',str(job.get(x)))
                language_detector=detect_langs(str(BeautifulSoup(job[x],'html.parser').get_text()))
                break
    except Exception as e:
        return {'error':{'another_language_job':"Exception Raised at detetcting language {} and Job title is {job}".format(str(e),job=job.get('job_title'))}}
    if len(language_detector)>1:
        return {'error':{'another_language_job':str(language_detector)}}
    else:
        content_spliter=str(language_detector[0]).split(':')
        if content_spliter[0]=='en':
            if '0.9999' not in content_spliter[1]:
                return {'error':{'another_language_job':str(language_detector)}}
        else:
            return {'error':{'another_language_job':str(language_detector)}}
    #identifying correct locations
    if pin==None:
        if 'remote'!=job['job_location'].lower().strip():
            job.update(locationIdentifier(job['job_location'].replace('Headquarters','').replace('Various Locations','').replace('Airport','').replace('school','')))
    for column_name in ['job_description','job_roles_responsibilities','qualifications','job_requirements']:
        if job.get(column_name)!=None:
            job[column_name]=HtmlParser(job.get(column_name),job)
    if 'taleo' in job.get('apply_link'):
        if '?' not in job.get('apply_link'):
            job['apply_link']=job.get('apply_link')+"?job="+str(job.get('job_id'))
        else:
            job['apply_link']=job.get('apply_link')+"&job="+str(job.get('job_id'))
    job['scrapped_date']=str(datetime.datetime.now())
    return {'type':type,'job':job}

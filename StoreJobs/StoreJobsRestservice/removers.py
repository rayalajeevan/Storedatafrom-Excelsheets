import datetime
import re
import unicodedata
from bs4 import BeautifulSoup
from dateutil import parser
from copy import deepcopy
from fuzzywuzzy import fuzz
import time
import json
import requests
from StoreJobsRestservice.models import Locations,BeautifyCompanyJobs
from langdetect import detect,detect_langs
from StoreJobsRestservice.instructions import Instructions,InstructionsForAll
def locationIdentifier(org_location):
    job_location=None
    country_type=None
    if 'remote' not  in str(org_location).lower():

        location=deepcopy(org_location.strip().replace('#','').replace('&',''))
        location=location.replace(',','>').replace(';','>')
        locationSpliter=[x.strip() for x in location.split('>') if x.strip() !='']
        if len(locationSpliter)!=1:
            orginal_location=get_location_from_database(locationSpliter)
            if orginal_location.get('location')==0:
                orginal_location=get_location_from_googleApi(org_location.replace('#','').replace('&',' '))
        else:
            orginal_location=get_location_from_googleApi(org_location.replace('#','').replace('&',' '))
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
                    obj_list=Locations.objects.filter(city=city,country_code=country_type)
                    if len(obj_list)!=0:
                        state=obj_list[0].state_code
                        job_location=city+", "+state
                    else:
                        job_location=city+", "+country_type
                except:
                    job_location=city+", "+state
        else:
            job_location=org_location
            country_type=None
    else:
        job_location="Remote"
        country_type="Remote"
    return {'job_location':job_location,'country_type':country_type,'scrapped_location':org_location}
def locationReplacer(data):
    data=data.replace('Clearwater',' ')
    data=data.replace('Airport',' ')
    return data
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
        location_request=requests.get('http://api.geonames.org/searchJSON?q={location}&maxRows=1&username=optncpt'.format(location=location.replace('#','')))
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
                    return {"location":{'city':locationReplacer(city),'state_code':state_code,'country_type':country_type}}
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
def get_postalCode_from_googleApi(location):
    """
     get_postalCode_from_googleApi
     this function get the matched postal_code from google api
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
        location_request=requests.get('http://api.geonames.org/postalCodeSearchJSON?placename={location}&maxRows=3&username=optncpt'.format(location=location.replace('#','')))
    except Exception as e:
        print(" get_postalCode_from_googleApi got Error So Sleeping for 20")
        time.sleep(20)
        print(str(e))
        return get_postalCode_from_googleApi(location)
    if location_request.status_code==200:
        location_data=location_request.json()
        try:
            if len(location_data.get('postalCodes'))!=0 or location_data.get('postalCodes')!=None:
                for postal_code in location_data.get('postalCodes')[0:1]:
                    if postal_code.get('countryCode')=="US" or postal_code.get('countryCode')=="IN":
                        postalCode_data=Locations.objects.filter(postal_code=postal_code.get('postalCode'),country_code=postal_code.get('countryCode'))
                        if len(postalCode_data)!=0:
                            city=postalCode_data[0].city
                            state_code=postalCode_data[0].state_code
                            country_type=postal_code.get('countryCode')
                            return {"location":{'city':city,'state_code':state_code,'country_type':country_type}}
            else:
                return {'location':0}
            if city==None and state_code==None and country_type==None:
                return {'location':0}
        except Exception as e:
            print("get_postalCode_from_googleApi got error so sleeping 20 secs")
            time.sleep(20)
            print(str(e))
            return get_postalCode_from_googleApi(location)
    else:
        print("get_postalCode_from_googleApi not got 200 status So Sleeping for 20 secs")
        time.sleep(20)
        return get_postalCode_from_googleApi(location)
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
def BeautifyJobs(data):
    soup=BeautifulSoup(data,'html.parser')
    for x in soup.findAll():
        if x.name=='table':
            x.name='div'
        if x.name=='tr':
            x.name='div'
        if x.name=='td':
            x.name='p'
    return str(soup)
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
            value=int(value)*31
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
            value=31
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'year ' in date.lower():
            value=365
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
def detect_job_type(job_type):
    if job_type!=None and str(job_type).strip()!='':
        detected_job_type=None
        job_type_items=({'Full Time':
        ('full time','full-time','Full-time','Full-time (FT)','Full Time Regular','Casual / On Call','FULL_TIME','permanent')},
        {'Part Time':('part time','part-time','Temporary','PART_TIME','half-time','half time','parttime')},
        {'Entry Level':('graduate','Tech Grad','fresher','entry level','College Grad')},
        {'Internship':('intern','intern.','intern,','intern ','internship','internship.','internship,','internship ','fellowship','fellowship.','fellowship,','fellowship ','aperentship','aperentship.','aperentship,','aperentship ','trainee','trainee.','trainee,','trainee ','apprenticeship','apprenticeship.','apprenticeship,','apprenticeship ')},
        {'Contract':('contract',)},
        {'Third Party':('third party',)}
        )
        for item in job_type_items:
            for key,value in item.items():
                for type_item in value:
                    if type_item.lower() in job_type.lower().strip():
                        detected_job_type=key
                        break
                if detected_job_type!=None:
                    break
            if detected_job_type!=None:
                    break
        if detected_job_type==None:
            detected_job_type='Full Time'
        return detected_job_type
    else:
        return 'Full Time'






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
def remving_extraSpacesHtmlContent(data):
    """
    removing unwanted extra spaces in Html Content
    """
    inline_elements=('a','abbr','acronym','audio','b','bdo','big','bdi','canvas','cite','code','data','datalist','del','dfn','em','embed','i','iframe','img','input','ins',
                     'kbd','label','map','mark','meter','noscript','object','output','picture','progress','q','ruby','s','samp','script','select','slot','small','span','strong','sub','sup','t'
                     'template','svg','textarea','time','u','tt','var','video','wbr',)
    soup=BeautifulSoup(data,'html.parser')
    for x in soup.findAll():
        if x.name!='br':
            if len(x.getText().strip())==0:
                if x.nextSibling!=None and x.find_next_sibling(x.nextSibling.name)!=None:
                    if len(x.find_next_sibling(x.nextSibling.name).getText().strip())==0:
                        x.find_next_sibling(x.nextSibling.name).decompose()
                if  x.previous_element!=None   and x.find_previous_sibling(x.previous_element.name)!=None :
                    if len(x.find_previous_sibling(x.previous_element.name).get_text().strip())==0:
                        x.find_previous_sibling(x.previous_element.name).decompose()
    for x in soup.findAll('br'):
        if x.parent!=None and x.parent.name!='p' and len(x.parent.getText())!=0:
            if x.nextSibling!=None and x.nextSibling.name=='br':
                x.find_next_sibling(x.nextSibling.name).decompose()
            if x.previous_element!=None and x.previous_element.name=='br':
                x.find_previous_sibling(x.previous_element.name).decompose()
            if x.find_parent('p')!=None and len(x.find_parent('p').getText().strip())==0:
                x.find_parent('p').decompose()
    for x in soup.findAll():
        enabled=True
        if x.name in inline_elements:
            enabled=False
        if enabled==True:
            if (x.nextSibling!=None and x.nextSibling.name=='br') or (x.nextSibling!=None and x.find_next_sibling(x.nextSibling.name)!=None and len(x.find_next_sibling(x.nextSibling.name).get_text().strip())==0):
                 x.find_next_sibling(x.nextSibling.name).decompose()
    return BeautifyJobs(str(soup))
# def detect_experince_level(job):
#     items=('senior','manager','fresher',)

def replacer(data):
    return data
def HtmlParser(data,job={}):
    items=  ('Role opening date:','OPENING DATE:','Salary:','Opening Date for Application:','Closing Date for Applications: ','JOB TYPE:','CLOSING DATE:','REPORTING TO','DATE:','Date posted','Job ID','GRADE:','DEADLINE TO APPLY:','Date Posted:','FLSA Designation:','Reports to:','Date written/ revised:','Date Created/Revised:','Job Description for:','Deadline','Salary','Deadline:','Salary:','location:','locations:','work location(s):','team:', 'reports to:','title:','hours:','pay rate:','Req. ID:','Recruiter:','Role:','Position Location:','Reports To:','Allocation Specialist','Business Unit:','Supervision:','Supervision:','Full Time, Fixed Term - 12 Months','Requisition ID:','Position Title:','Project:','Relocation Authorized:','Position to be Panel Interviewed?','Grade:','Work Authorization:','Other Requirements:','Company:','Req ID:','Date:','Start Date:','Work type:','Categories:','Job no:','Contract:','Profile :','Scope :','DEPARTMENT:','BASE RATE OF PAY:','SHIFT:','Your future manager :','Scope :','Reporting Relationship','Employee Status:','Work Location:','Role Location:','Role Type:','Shift Schedule:','Rostered Hours:','Hours and shift type','Job Family:','TITLE:','FACILITY:','START DATE:','FLSA CATEGORY:','Reports To:','Supervisor:',"Role:",'Permanent Position','Schedule:','Audition Date & Time:','permanent position','Posting Number:','Position Type:','Classification:','Status:','Department:','Hours:','Reports to:','POSITION TITLE','POSITION LOCATION','POSITION HOURS','Position Title:','Location:','POSITION','LOCATION','Posting Notes:','Job Title:','Req. ID:','Contract Type','HOURS:','WAGE:','Role Location:','Role opening date',
    'Closing date for applications:','Req. ID:','Hiring Manager:','Relocation Level:')
    items_starts_with=('POSITION:','Location:','Department:','Temporary position (1 year)','Bass (1 year appointment)','Position:','Shift:')
    itemsNotEqual=('POSITION SUMMARY','OVERVIEW OF POSITION:','POSITION PURPOSE','About the Company:','REQUIREMENTS FOR POSITION:','Our Company:'
    'Weekday Day Hours:','Weekday Night Hours:','Weekend Day Hours:','Weekend Night Hours:','Salary range:','Our Company:')
    soup=BeautifulSoup(data,"html.parser")
    for tag in soup.findAll():
        try:
            if tag.get('style')=='display:none;' or tag.get('style')=='display: none;':
                tag.decompose()
        except AttributeError:
            continue
    datarefineer=('primary_location',
                'recruiter_name',
                'job_id')
    datarefineer_identifier=('class','id','name')
    for x in datarefineer_identifier:
        for y in datarefineer:
            for refine in soup.findAll({x:y}):
                refine.decompose()
    for x in soup.findAll('a'):
        if 'http' in x.get_text().strip().lower() or 'www.' in x.get_text().strip().lower() or '.org' in x.get_text().strip().lower() or '.in' in x.get_text().strip().lower() or '.com' in x.get_text().strip().lower():
            x.decompose()
            continue
        x.attrs=None
    RemovableTags=('button','submit','img','script','path','svg','input','hr','select','iframe','textarea')
    for tag in RemovableTags:
        for x in soup.findAll(tag):
            if x!=None:
                x.decompose()
    for x in (soup.find('div',{'video-container small-video centerOrient':'true'}),soup.find('div',{'class':'iCIMS_JobOptions'}),soup.find('div',{'class':'iCIMS_JobHeaderGroup'}),soup.find('span',{'class':'LimelightEmbeddedPlayer'})):
        if x!=None:
            x.decompose()
    REMOVE_ATTRIBUTES = ('lang','language','onmouseover','onmouseout','script','font','dir','face','color','hspace','border','valign','align','background','bgcolor','link','vlink','alink','href','id','src','type','border','align')
    for attr in REMOVE_ATTRIBUTES:
        try:
            for tag in soup.findAll(attribute=True):
                if tag!=None:
                    del(tag[attribute])
        except AttributeError:
            continue
    for tag in soup.findAll(True):
        tag.attrs=None
    for x in soup.findAll():
         if len(x.findChildren())==0:
            if '#' in x.getText().strip() and len(x.getText().strip())<=20:
                x.decompose()
                break
            if '*' in x.getText().strip() and  len(x.getText().strip())<=20:
                 x.decompose()
                 break
    removed_elements=[]
    removed_tags=[]
    for x in soup.findAll():
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_title','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            removed_tags.append('job Title:')
            removed_tags.append('Title:')
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_location','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            removed_tags.append('job location')
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('functional_area','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            removed_tags.append('functional area')
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_id','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            removed_tags.append('job id')
            x.decompose()
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_type','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            removed_tags.append('job type')
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('work_shift','qwertyuiopasdfghjklzxcvbnm').lower())>50:
            x.decompose()
            removed_tags.append('work_shift')
            continue
        if fuzz.ratio(x.getText().strip().lower(),job.get('job_title','qwertyuiopasdfghjklzxcvbnm').lower()+" "+job.get('job_location','qwertyuiopasdfghjklzxcvbnm').lower())>50:
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
        for item in items:
            if item=='Role opening date:':
                if item.strip() in x.getText().strip():
                    if x.parent!=None and len(x.parent.get_text().strip())<=70:
                        true=True
                        for item1 in itemsNotEqual:
                            if item1.strip() in x.parent.getText().strip():
                                true=False
                        if true==True:
                            print("True2")
                            if len(x.parent.get_text())!=len(x.getText().strip()):
                                removed_elements.append(str(x.parent))
                                x.parent.decompose()
                    else:
                        if len(x.get_text().strip())<=100:
                            true=True
                            for item in itemsNotEqual:
                                if item.strip() in x.getText().strip():
                                    true=False
                            if true==True:
                                removed_elements.append(str(x))
                                x.decompose()
    soup=BeautifulSoup(str(soup),'html.parser')
    for tag in soup.findAll():
        for item in removed_tags:
            if item in tag.getText() or fuzz.ratio(item,tag.getText())>60:
                try:
                    tag.replace_with('')
                    removed_elements.append(str(tag))
                except:
                    tag.decompose()
                    removed_elements.append(str(tag))
    for tag in soup.findAll():
        for item in items:
            if item in tag.getText() and len(tag.getText())<=100:
                true=True
                for item in itemsNotEqual:
                    if item.strip() in tag.getText().strip():
                        true=False
                if true==True:
                    removed_elements.append(str(tag))
                    tag.decompose()
    for tag in soup.findAll():
        for item in items_starts_with:
            if tag.getText().strip().startswith(item) and len(tag.getText())<100:
                removed_elements.append(str(tag))
                tag.decompose()
    for ele in removed_elements:
        soup=str(soup)+str(ele)
    soup=str(soup).replace('&#8203','').replace('Duties: JOB DESCRIPTION','')
    return remving_extraSpacesHtmlContent(str(soup))
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
    #detect Job type
    job['job_type']=detect_job_type(job.get('job_type'))
    #get location with postal_code
    pin=None
    if job.get('pin')!=None:
        data=Locations.objects.filter(postal_code=job.get('pin'))
        if len(data)!=0:
            job['job_location']=data[0].city+", "+data[0].state_code
            job['country_type']=data[0].country_code
            pin="modified"
            del job['pin']

    #setting up city and state into location

    if job.get('job_location')==None:
        for column_name in ['city','state','country']:
            if job.get(column_name)!=None:
                if job.get('job_location')==None:
                    job['job_location']=job.get(column_name)
                else:
                    job['job_location']=job['job_location']+" "+job.get(column_name)
                del job[column_name]
    #validateing column names

    for column_name in ['job_title','company_info_id','company_name','job_location','apply_link']:
        if job.get(column_name)==None or str(job.get(column_name))=='None':
            return {'error':{'column_name_error':'{} column name is missing'.format(column_name)}}
        elif job.get(column_name)=='':
            return {'error':{'column_data_error':'{} column name exist but data is missing'.format(column_name)}}
    if job.get('job_description')==None and job.get('job_roles_responsibilities')==None and job.get('qualifications')==None and job.get('job_requirements')==None:
        return {'error':{'column_name_error':"['job_description','job_roles_responsibilities','qualifications','job_requirements'] atleast one of the column must exist "}}
    #setting the posted date in database information

    job['posted_date']=str(validatos(job.get('posted_date')))

    # detetcting JOB_TYPE
    job_type_list=('intern','part-time','full-time','part time','full time','regular','permanent','contract','half-time','half time','parttime','fulltime','entry level')
    for type in job_type_list:
        if type!='entry level':
            if job.get('job_type','@a1>2<').lower().strip() in type:
                job['job_type']=type.capitalize()
                break
        else:
            if  job.get('job_type','@a1>2<').lower().strip()=='college grad':
                job['job_type']=type.capitalize()
                break
            if job.get('job_type','@a1>2<').lower().strip() in type:
                job['job_type']=type.capitalize()
                break
    if job.get('job_type')==None:
        job['job_type']='Full Time'
    #error throughing when postion was closed

    if 'position has been closed' in str(job.get('job_description')).lower():
        return {'error':{'position was closed':'Postion has been closed '}}

    #Beautify the Data-->removing unwanted data from particular company

    Beautify_objects=BeautifyCompanyJobs.objects.filter(company_info_id=job['company_info_id'])
    if len(Beautify_objects)!=0:
        for obj in Beautify_objects:
            if obj.attrs==None and obj.keywords==None and obj.html_tags==None and obj.apply_link==None:
                job =Instructions(obj.instruction_id,job).method_caller()
            else:
                query={}
                for column_name in ('html_tags','attrs','keywords','apply_link'):
                    if column_name=='attrs' and obj.__dict__.get(column_name)!=None:
                        query[column_name]=json.loads(obj.__dict__.get(column_name))
                        continue
                    if obj.__dict__.get(column_name)!=None:
                        query[column_name]=obj.__dict__.get(column_name)
                incobj=InstructionsForAll(job)
                job=incobj.rule_for_all(**query)

    #identifying the internship or jobs
    type=None
    for value in (job['job_title'],job.get('job_type'),job.get('functional_area')):
        value=str(value).strip()
        for identifiers in ('intern','intern.','intern,','intern ','internship','internship.','internship,','internship ','fellowship','fellowship.','fellowship,','fellowship ','aperentship','aperentship.','aperentship,','aperentship ','trainee','trainee.','trainee,','trainee ','apprenticeship','apprenticeship.','apprenticeship,','apprenticeship '):
            if identifiers in [str(x).lower().strip() for x in value.split()]:
                type="INI"
    if type==None:
        type='JOB'

    #identifying the another languages job_description
    for item in ['Please refer to the corresponding language to initiate your application.','This job posting is only available in German language','This job posting is only available in German language','Sorry, this position has been filled']:
        if str(item).lower().strip() in str(job.get('job_description')).lower().strip():
            return {'error':{'another_language_job':'This job posting is only available in the language of the country where the position is located. Please refer to the corresponding language to initiate your application.'}}
    try:
        for x in ('job_description','job_roles_responsibilities','qualifications'):
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
            job.update(locationIdentifier(job['job_location'].replace('Headquarters','').replace('Various Locations','multiple locations').replace('Airport','').replace('school','')))
    for column_name in ('job_description','job_roles_responsibilities','qualifications','job_requirements'):
        if job.get(column_name)!=None:
            job[column_name]=HtmlParser(job.get(column_name),job)
    if 'taleo' in job.get('apply_link'):
        if '?' not in job.get('apply_link'):
            job['apply_link']=job.get('apply_link')+"?job="+str(job.get('job_id'))
        else:
            job['apply_link']=job.get('apply_link')+"&job="+str(job.get('job_id'))
    job['scrapped_date']=str(datetime.datetime.now())
    return {'type':type,'job':job}

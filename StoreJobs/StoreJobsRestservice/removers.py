import datetime
import re
import unicodedata
from bs4 import BeautifulSoup
from dateutil import parser
from copy import deepcopy
from fuzzywuzzy import fuzz
import time
import copy as cp
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
        except Exception as exc:
            print("get_location_from_googleApi got error so sleeping 20 secs",Log.EXCEPTION.value)
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
    span_list=list()
    NegtiveTags=('br','i')
    for x in soup.findAll():
        if x.name=='table':
            x.name='div'
        if x.name=='tr':
            x.name='div'
        if x.name=='td':
            x.name='p'
        for k in ['h1','h2','h3','h4']:
            if x.name==k:
                x.name='h5'
        if x.name=='font':
            x.name='span'
        # if x.getText().strip()=='' and x.name not in NegtiveTags and len(x.findChildren())==0:
        #     x.name='br'
    #     if len(x.getText().strip())<=30 and ':' in x.getText() and len(x.getText().strip())>3 :
    #         if len(x.findChildren())==0:
    #             span_list.append(str(x))
    # for x in span_list:
    #     soup=str(soup).replace(x,"<span class='newLine'><b>{}</b></span>".format(x))
    soup=soup.prettify(formatter=None)  
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
        if 'days' in date.lower() or date.replace(str(value).strip(),'').strip().lower()=='ds':
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'day' in date.lower()or date.replace(str(value).strip(),'').strip().lower()=='d':
            date=datetime.datetime.now()-datetime.timedelta(days=int(value))
        elif 'weeks' in date.lower()or date.replace(str(value).strip(),'').strip().lower()=='w' or date.replace(str(value).strip(),'').strip().lower()=='ws':
            date=datetime.datetime.now()-datetime.timedelta(weeks=int(value))
        elif 'months' in date.lower() or date.replace(str(value).strip(),'').strip().lower()=='m' or date.replace(str(value).strip(),'').strip().lower()=='ms':
            value=int(value)*31
            date=datetime.datetime.now()-datetime.timedelta(days=value)
        elif 'years' in date.lower()or date.replace(str(value).strip(),'').strip().lower()=='ys' or date.replace(str(value).strip(),'').strip().lower()=='y':
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
def validatos(date,*args,**kwrgs):
    datestr=None
    if  date!=None and date!=float('nan') and date!="" and date!='NULL' and date !="null" and date.strip()!="Not Specified" :
        date=date.strip()
        if 'yesterday' in date.lower():
            datestr=datetime.datetime.now()-datetime.timedelta(days=1)
            return datestr
        if 'today' in date.lower():
            return datetime.datetime.now()
        if 'week' in date.lower() or 'day' in date.lower() or 'year' in date.lower() or 'minutes' in date.lower() or 'hour' in date.lower() or 'month' in date.lower() or 'hr' in date.lower() or 'min' in date.lower() or 'sec' in date.lower() or " ".join(re.findall("[a-zA-Z]+",date)).strip() in ('d','ds','w','ws','m','ms'):
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
def detect_job_type(job_type,job):
    job_type_items=({'Full-time':
        ('full time','full-time','Full-time','Full-time (FT)','Full Time Regular','Casual / On Call','FULL_TIME','permanent')},
        {'Part-time':('part time','part-time','Temporary','PART_TIME','half-time','half time','parttime')},
        {'Entry-Level':('graduate ','Tech Grad','fresher ','Entry-Level','College Grad')},
        {'Contract':('contract ',)},
        {'Third Party':('third party ',)}
        )
    NegtiveMatches=(' no ',' not ',' non '," don't "," aren't "," isn't " ," wasn't "," weren't "," haven't ","hasn't",
        "hadn't","doesn't","didn't","can't","couldn't","mustn't","needn't","won't","wouldn't","shan't","shouldn't",
        "oughtn't ")
    if job_type!=None and str(job_type).strip()!='':
        detected_job_type=None
        job_type=job_type.split()
        job_type=' '.join(job_type)
        for item in ('intern ', 'intern,','intern.','intern!','internship'):
            if item in job_type.lower().strip():
                detected_job_type="Internship"
        if job_type.lower()=="intern":
            detected_job_type="Internship"   
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

        return detected_job_type
    else:
        detected_job_type=None
        split_data=[x for x in str(job).split(',') if x!='' ]
        matched_list=list()
        for x  in range(len(split_data)):
            for  y in [item  for obj in job_type_items[0:5:] for items in obj.values() for item in items]:
                if y in split_data[x]:
                    for not_item in NegtiveMatches:
                       if not_item not in split_data[x].split(y)[0][-20::]:
                           matched_list.append(y)
                           break
        for x in matched_list:
            for obj in job_type_items[0:5]:
                for key,values in obj.items():
                    if x in values:
                        detected_job_type=key
                        break
        return detected_job_type




def string_error(data,type1="desc",*args,**kwrgs):
    if data!='' or data!='NULL' or data!='null' or data!=None or data!="None":
        try:
            if type1=="not_desc":
                unicode=unicodedata.normalize('NFKD', data).encode('ascii','ignore').decode("utf-8")
            else:
                unicode=unicodedata.normalize('NFKD', data).encode().decode("utf-8")
            return unicode
        except:
           return data
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
    NegtiveTags=('br','i')
    for x in soup.findAll():
        if x.name not in NegtiveTags:
            if len(x.getText().strip())==0:
                if x.nextSibling!=None and x.find_next_sibling(x.nextSibling.name)!=None:
                    if len(x.find_next_sibling(x.nextSibling.name).getText().strip())==0:
                        x.find_next_sibling(x.nextSibling.name).decompose()
                if  x.previous_element!=None   and x.find_previous_sibling(x.previous_element.name)!=None :
                    if  x.find_previous_sibling(x.previous_element.name).name=='br' and x.find_previous_sibling(x.previous_element.name).parent.name=='p':
                        continue
                    if len(x.find_previous_sibling(x.previous_element.name).get_text().strip())==0:
                        x.find_previous_sibling(x.previous_element.name).decompose()
    for x in soup.findAll('br'):
        if x.parent!=None and x.parent.name!='p' and len(x.parent.getText())!=0:
            if x.nextSibling!=None and x.nextSibling.name=='br':
                if x.find_next_sibling(x.nextSibling.name)!=None:
                    x.find_next_sibling(x.nextSibling.name).decompose()
            if x.previous_element!=None and x.previous_element.name=='br':
                if x.find_previous_sibling(x.previous_element.name)!=None:
                    x.find_previous_sibling(x.previous_element.name).decompose()
            if x.find_parent('p')!=None and len(x.find_parent('p').getText().strip())==0:
                if  len(x.find_parent('p').getText().strip())!=0:
                    x.find_parent('p').decompose()
    for x in soup.findAll('li'):
        for y in x.findChildren():
            if y.name=='br':
                y.decompose()
    for x in range(10):
        soup=break_replacer(str(soup))  
    return soup    

def break_replacer(data):
    break_tags=('<br>',"<br/>","<br\>"," <br>"," <br/>"," <br\>","<br> ","<br/> ","<br\> ","  <br>","  <br/>","  <br\>","<br>&nbsp;<br>","<br> &nbsp; <br>","<br>&nbsp;","<br> &nbsp;","<br>&nbsp; ","<br>&nbsp; ",r"<br>\n<br>")
    for x in break_tags:
        tag=''
        a=10
        for z in range(10):
            for y in range(a):
                tag=tag+x
            a-=1
            data=data.replace(tag,"<br>")
            tag=""        
    return data        
            
        


def replacer(data):
    return data
def HtmlParser(data,job={}):
    data=re.sub('\s+',' ',str(data))
    data=string_error(data)
    # items=('Type:','PRIMARY PURPOSE OF POSITION','Job   Location','Reports Directly To:','Title:','Job  Type','Overtime  Status','Employee  Status','Role opening date:','OPENING DATE:','Primary Location','Other Locations','Full-time / Part-time','Employee Status','Overtime Status','Job Type','Travel:','Salary:','Opening Date for Application:','Closing Date for Applications: ','JOB TYPE:','CLOSING DATE:','REPORTING TO','DATE:','Date posted','Job ID','GRADE:','DEADLINE TO APPLY:','Date Posted:','FLSA Designation:','Reports to:','Date written/ revised:','Date Created/Revised:','Job Description for:','Deadline','Deadline:','Salary:','location:','locations:','work location(s):','team:', 'reports to:','title:','hours:','pay rate:','Req. ID:','Recruiter:','Role:','Position Location:','Reports To:','Allocation Specialist','Business Unit:','Supervision:','Supervision:','Full Time, Fixed Term - 12 Months','Requisition ID:','Position Title:','Project:','Relocation Authorized:','Position to be Panel Interviewed?','Grade:','Work Authorization:','Other Requirements:','Req ID:','Date:','Start Date:','Work type:','Categories:','Job no:','Contract:','Profile :','Scope :','DEPARTMENT:','BASE RATE OF PAY:','SHIFT:','Your future manager :','Scope :','Reporting Relationship','Employee Status:','Work Location:','Role Location:','Role Type:','Shift Schedule:','Rostered Hours:','Hours and shift type','Job Family:','TITLE:','FACILITY:','START DATE:','FLSA CATEGORY:','Reports To:','Supervisor:',"Role:",'Permanent Position','Schedule:','Audition Date & Time:','permanent position','Posting Number:','Position Type:','Classification:','Status:','Department:','Hours:','Reports to:','POSITION TITLE','POSITION LOCATION','POSITION HOURS','Position Title:','Location:','POSITION','LOCATION','Posting Notes:','Job Title:','Req. ID:','Contract Type','HOURS:','WAGE:','Role Location:','Role opening date',
    # 'Closing date for applications:','Posting ID:','City:','Req. ID:','Division:','Unit:','Full Performance level:','Number of Positions Available:','Duration:','Hiring Manager:','Relocation Level:','Job Number:','Pub Date:','Job Reference Code','Job/Requisition ID:','Location Name:','Education Level:','Relevant Experience Level:','Employee Group:','Employee Subgroup:','Primary  Location','Other  Locations','Full-time  /  Part-time')
    # items_starts_with=('Job Function:','Level','Job Location','Position Type','Education Level','POSITION:','Department:','Temporary position (1 year)',
    # 'Bass (1 year appointmenLocation Name:t)','Position:','Shift:')
    # itemsNotEqual=('Working hours:','PRIMARY OBJECTIVE OF POSITION:','About This Role:','THIS POSITION HAS AN EDUCATION REQUIREMENT:','POSITION PURPOSE:','Travel, Meetings & Events (including Brand, Marketing and Communications)','DIRECTLY SUPERVISES (PLEASE LIST POSITION TITLES','SPECIAL REQUIREMENTS FOR THIS POSITION:','Travel role','POSITION REQUIRMENTS:','POSITION REQUIREMENTS','Level II:','Level III:','Salary Information:','Travel Required:','Level I to Level III is considered a progression and is approved by the appropriate manager.','Level I:','POSITION PROFILE','POSITION DIMENSIONS AND QUALIFICATIONS','POSITION SUMMARY','Reporting Relationships:','Core Duties and Responsibilities:','OVERVIEW OF POSITION:','POSITION PURPOSE','About the Company:','REQUIREMENTS FOR POSITION:','Our Company:'
    # 'Weekday Day Hours:','Weekday Night Hours:','Weekend Day Hours:','Weekend Night Hours:','Salary range:',"""Our Company:""",'Employment Type:')
    soup=BeautifulSoup(data,"html.parser")
    for tag in soup.findAll():
        try:
            if tag.get('style')=='display:none;' or tag.get('style')=='display: none;':
                tag.decompose()
            if tag.get('style')=='font-weight: bold':
                tag.name='b'
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
                    del(tag[attr])
        except AttributeError:
            continue
    for tag in soup.findAll(True):
        tag.attrs=None
    soup=BeautifulSoup(str(soup),'html.parser')
    soup=replacer(str(soup))
    return remving_extraSpacesHtmlContent(BeautifyJobs(str(soup)))
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
                    new_jobData["FLSA_status"]=string_error(value,'not_desc')
                    continue
                if 'itar'==key:
                    new_jobData["ITAR"]=string_error(value,'not_desc')
                    continue
                new_jobData[key.lower()]=value
    return new_jobData
def detect_experience_level(experience,data,job):
    detected_experience_level=None
    exp_levels=list()
    deteted_keywords=('senior developer','senior manager','technical lead',' lead ')
    for x in deteted_keywords:
        if job.get('job_title')!=None and x in job.get('job_title').lower():
            return 'Senior Level'
    if experience==None:
        experience_level_items=({'Senior Level':('senior developer','senior manager',' lead ','lead ','lead.','lead,')},{'Entry-Level':('fresher',)})
        NegtiveMatches=(' no ',' not ',' non '," don't "," aren't "," isn't " ," wasn't "," weren't "," haven't ","hasn't",
        "hadn't","doesn't","didn't","can't","couldn't","mustn't","needn't","won't","wouldn't","shan't","shouldn't",
        "oughtn't ")
        split_data=[x for x in str(data).split(',') if x!='' ]
        matched_list=list()
        for x  in range(len(split_data)):
            for  y in [item  for obj in experience_level_items for items in obj.values() for item in items]:
                if y in split_data[x]:
                    for not_item in NegtiveMatches:
                       if not_item not in split_data[x].split(y)[0][-20::]:
                           matched_list.append(y)
                           break
        for x in matched_list:
            for obj in experience_level_items:
                for key,values in obj.items():
                    if x in values:
                        detected_experience_level=key
                        break
        if detected_experience_level!=None:
            exp_levels.append(detected_experience_level)
            return  exp_levels
        return None
    else:
        numbers=[]
        exp=None
        if '-' in experience:
            experience=experience.lower().replace(' ','').replace('year(s)','').replace('year','')
            minum=int(experience.split('-')[0])
            maxum=int(experience.split('-')[1])
            exper_levels={0:'Entry-Level',1:'Entry-Level',2:'Entry-Level',3:"Mid Level",4:"Mid Level",5:"Mid Level",6:"Mid Level"}
            for i in range(minum,maxum):
                try:
                    if exper_levels[i] not in exp_levels:
                       exp_levels.append(exper_levels[i])
                except:
                    if 'Senior Level' not in exp_levels:
                        exp_levels.append('Senior Level')
                        break
            return exp_levels
        else:
            expression=re.compile(r'\d+')
            search=re.search(expression,experience)
            if search!=None:
                exp=search.group()
            if exp==None:
                return None
            else:
                numbers.append(int(exp))
        if len(numbers)!=0:
            if max(numbers)>=0 and max(numbers)<3:
                exp_levels.append('Entry-Level')
            elif  max(numbers)>=3 and max(numbers)<7:
                exp_levels.append('Mid Level')
            elif  max(numbers)>=7:
                exp_levels.append('Senior Level')
                
                
        else:
            return None
        return  exp_levels
def detect_experince(data,type="html"):
    
    if type=='html':
        split_data=(x.lower().replace(',','').replace('.','').replace(':','').replace(';','') for x in data)
        split_data=list((y for x in split_data for y in x.split()))
    else:
        print(data,"ksjfkjsgkjsgfkjsvhkbfs")
        data=data+" experience"
        split_data=[x.lower().replace(',','').replace('.','').replace(':','').replace(';','') for x in data.split() if x.strip()!='']
    keywords=('years','year')
    notMatchedKeywords=('age','started','ended','we have achieved four straight',
    'ranking','within the Vault Consulting','Some may think were old','degree','education',"mba","MBA")
    index=list()
    replcers=(',','.',':')
    string=None

    for x in range(len(list(split_data))):
        # if 'years' in split_data[x].strip():
        #     print(split_data[:x+20])
        for y in keywords:
            if y in split_data[x].strip():
                for z in split_data[x:x+20]:
                    if ('experience' in z and x not in index) or ('expertise' in z and x not in index)  :
                        index.append(x)
                        break
    exp=None
    exp_list=list()
    indexer=None
    count=0
    year_dict={1:'one',2:'two',3:'three',4:'four',5:'five',6:'six' ,7:'seven',8:'eight',9:'nine',10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',20:'twenty'}
    for  x in index:
        count+=1
        if count>10:
            break
        if indexer==None:
            indexer=4
        try:
            if x==1:
                string=" ".join(y for y in split_data[0:x:] if y!='')+" "
                enabled=True
                for y in notMatchedKeywords:
                    if '@AUTOMATION' in string:
                        if y in string.split() and string.index('@AUTOMATION')< string.index(y):
                            enabled=False
                    else:
                        if y in string.split():
                            enabled=False      
            if x>1:
                string=" ".join(y for y in split_data[x-indexer:x+indexer:] if y!='')+" "
                enabled=True
                for y in notMatchedKeywords:
                    if y in string.split():
                        enabled=False
                string=" ".join(y for y in split_data[x-indexer:x+1:] if y!='')+" "
                if len(string.strip().split())<3:
                    exp=None
                    indexer=indexer-1
                    index.append(x)
                    continue    
            if enabled==True:
                expression=re.compile(r'\d+-\d+|\d+- \d+|\d+ -\d+|\d+ ~ \d+')
                search=re.search(expression,string)
                if search!=None:
                    exp=search.group()
                    exp_list.append(exp)
                else:    
                    expression=re.compile(r'\d+ - \d+|\d+ to \d+|\d+to\d+|\d+to \d+')
                    search=re.search(expression,string)
                if search!=None:
                    exp=search.group()
                    exp_list.append(exp)
                else:
                    expression=re.compile(r'\d+')
                    search=re.search(expression,string)
                    if search!=None:
                        exp=search.group()
                        if int(exp)>25:
                            exp=None
                            indexer=indexer-1
                            index.append(x)
                            continue
                        exp_list.append(exp)
                if exp==None:
                    for key,value in year_dict.items():
                        if value in string.split():
                            exp=key
                            exp_list.append(exp)                                            
        except :pass
    if exp==None:
        return None
    exp=exp.replace('to','-').replace(" ",'')
    exp_list=[str(x).lower().replace('to','-').replace('~','-').replace(' ','') for x in exp_list if str(x).strip()!='']
    for x in exp_list:
        if '-' not in str(exp):
            if '-' in str(x):
                if int(exp)<int(x.replace(' ','').split('-')[1]):
                    exp=x
            else:
                if int(exp)<int(x):
                    exp=int(x)
        else:
            if '-' not in str(x):
                if int(exp.replace(' ','').split('-')[1])< int(x):
                    exp=int(x)
            else:
                if int(exp.replace(' ','').split('-')[1])<int(x.replace(' ','').split('-')[1]):
                    exp=x
    return str(exp)+" year(s)"
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
    back_up_fields={"job_description":"org_job_description","job_roles_responsibilities":"org_job_roles_responsibilities","qualifications":"org_qualifications"}
    for key,value in back_up_fields.items():
        if job.get(key)!=None:
            job[value]=cp.copy(job.get(key))
    # removing utf 8
    for key,value in job.items():
        if value!=None and key not in ('job_description','job_roles_responsibilities','qualifications','job_requirements'):
            job[key]=string_error(value,'not_desc')

    #detect Job type

    string=' '.join(value for key,value in job.items() if key  in ('job_description','job_roles_responsibilities','qualifications','job_requirements')and value!=None )
    soup=BeautifulSoup(string,'html.parser')
    type_job=detect_job_type(job.get('job_type'),soup.getText())
    if type_job!=None:
        type_job=json.dumps({"jobType":[type_job,]})
    job['job_type']=type_job
    #detect Experince
    split_data=list()
    for tag in soup.find_all():
        if tag.getText().strip()!='':
            split_data.append(str(tag.getText())+" @AUTOMATION")          
    if job.get('experience')!=None:
        job['experience']=detect_experince(job.get('experience'),"text")
    else:
        job['experience']=detect_experince(split_data)
    #detect Experince Level
    exp_level=detect_experience_level(job.get('experience'),soup.getText(),job)
    if exp_level!=None:
        exp_level=json.dumps({"experienceLevels":exp_level})
    job['experience_level']=exp_level
    #get location with postal_code
    pin=None
    if job.get('pin')!=None:
        job['pin']=str(job.get('pin'))
        if len(job.get('pin'))<5:
            for x in range(5-len(job.get('pin'))):
                job['pin']='0'+job.get('pin')
        data=Locations.objects.filter(postal_code=job.get('pin'))
        if len(data)!=0:
            job['job_location']=data[0].city+", "+data[0].state_code
            job['country_type']=data[0].country_code
            pin="modified"
            del job['pin']

    #setting up city and state into location

    if job.get('job_location')==None:
        for column_name in ['city','state','country']:
            if job.get(column_name)!=None and str(job.get(column_name))!='None'  and str(job.get(column_name)).lower()!='null':
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


    #error throughing when postion was closed

    if 'position has been closed' in str(job.get('job_description')).lower():
        return {'error':{'position was closed':'Postion has been closed '}}

    #Beautify the Data-->removing unwanted data from particular company

    Beautify_objects=BeautifyCompanyJobs.objects.filter(company_info_id=job['company_info_id'])
    if len(Beautify_objects)!=0:
        for obj in Beautify_objects:
            if obj.attrs==None and obj.keywords==None and obj.html_tags==None and obj.apply_link==None and obj.ul_li_tags==None:
                job =Instructions(obj.instruction_id,job).method_caller()
            else:
                query={}
                for column_name in ('html_tags','attrs','keywords','apply_link',"ul_li_tags"):
                    if (column_name=='attrs' or column_name=='ul_li_tags') and obj.__dict__.get(column_name)!=None:
                        query[column_name]=json.loads(obj.__dict__.get(column_name))
                        continue
                    if obj.__dict__.get(column_name)!=None:
                        query[column_name]=obj.__dict__.get(column_name)
                incobj=InstructionsForAll(job)
                job=incobj.rule_for_all(**query)

    #identifying the internship or jobs
    type=None
    for value in (job['job_title'],type_job,job.get('functional_area')):
        value=str(value).strip().replace('-',' ')

        value=value.replace(',',' ').replace('/',' ').replace(":",' ').replace(';',' ').replace('(',' ').replace(')',' ').replace('@',' ')
        for identifiers in ('intern','intern.','intern,','intern ','internships-','internships','internships.','internships,','internships ','internship-','internship','internship.','internship,','internship ','fellowship','fellowship.','fellowship,','fellowship ','fellowships','fellowships.','fellowships,','fellowships ','aperentship','aperentship.','aperentship,','aperentship ','trainee','trainee.','trainee,','trainee ','apprenticeship','apprenticeship.','apprenticeship,','apprenticeship ','aperentships','aperentships.','aperentships,','aperentships '):
            if identifiers in [str(x).lower().strip() for x in value.split()] :
                type="INI"
    if type==None:
        type='JOB'

    #identifying the another languages job_description
    for item in ['Please refer to the corresponding language to initiate your application.','This job posting is only available in German language','This job posting is only available in German language','Sorry, this position has been filled']:
        if str(item).lower().strip() in str(job.get('job_description')).lower().strip():
            return {'error':{'another_language_job':'This job posting is only available in the language of the country where the position is located. Please refer to the corresponding language to initiate your application.'}}
    language_detector=""
    try:
        for x in ('job_description','job_roles_responsibilities','qualifications'):
            if str(job.get(x))!="None":
                detect_data=re.sub('\s+',' ',str(job.get(x)))
                language_detector=detect_langs(str(BeautifulSoup(detect_data,'html.parser').get_text()))
                break
    except Exception as e:
        if 'No features in text' not in str(e):
            return {'error':{'another_language_job':"Exception Raised at detetcting language {} and Job title is {job}".format(str(e),job=job.get('job_title'))}}
    if len(language_detector)>1:
        return {'error':{'another_language_job':str(language_detector)}}
    elif len(language_detector)!=0:
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

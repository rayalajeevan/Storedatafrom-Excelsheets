from django.shortcuts import render
from django.views import View
import os
from django.http import JsonResponse
import json
import pandas as pd
from web.models import web_internship_jobs,company_jobs,company_info,companies_internship,StoreLocation,Beautify_company_jobs
from web.removers import validatos,string_error,replacer,dataModify
import requests
import json
from web.textfromHtml import text_from_html
from django.db.utils import DataError
from datetime import datetime
from langdetect import detect,detect_langs
import socket
import time
import requests
import json
import configparser
import datetime as dt
from copy import deepcopy
from bs4 import BeautifulSoup
import schedule
from web.instructions import Instructions
from threading import Thread
from fuzzywuzzy import fuzz
import webbrowser
import re
#developed By Jeevan Rayala
# dic=""""""
# job={'job_description':dic,'job_id':"CL416"}
# data=Instructions(35,job).method_caller()
# arr=open(r'C:\Users\Emphyd12146rjee1\Desktop\test.html','w')
# arr.write(str(data.get('job_description')).encode('ascii', 'ignore').decode("utf-8"))
# arr.close()
Config = configparser.RawConfigParser()
data='configuration.ini'
Config.read(data)
config={}
for each_sec in Config.sections():
    config=dict((k, v) for k, v in  Config.items(each_sec))
PATH=config.get('allpath')
DRIVE=config.get('drive')

class ExcelSheetData(View):
    def get(self,request,*args,**kwrgs):
        pathname=request.GET.get('fname')
        if pathname==None:
            return HttpResponse("Please provide Folder name")
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        ExceptionList=[]
        datesList=[]
        try:
            errornames=sheets_checking(request,pathname)
        except IndexError as Exception:
            return JsonResponse({'json':str(Exception)})
        type=None
        companies=0
        jobs=0
        updated=0
        interns=0
        internsdupli=0
        jobsdupli=0
        excelSheetList=os.listdir(PATH+pathname)
        finshed_task_sheets=[]
        columnnameError=[]
        columnnameErrorCount=0
        companies=0
        anotherLanguagesJobs=0
        anotherLanguagesJobs_data=[]
        error_rows=[]
        inserted_database_rows_count=0
        error_rows_count=0
        duplicate_job_rows=0
        for sheet in excelSheetList:
            parentlistDataframe=None
            childListDataFrame=None
            joblist=[]
            parentList=[]
            childList=[]
            path=PATH+pathname+"/{0}".format(sheet)
            list=pd.read_excel(path)
            if sheet not in finshed_task_sheets:
                companies+=1
                if 'parent' in sheet or 'child'in sheet:
                    if 'parent' in sheet:
                        sheet1=[sh for sh in excelSheetList if sheet.replace('parent','child')==sh][0]
                        path=PATH+pathname+"/{0}".format(sheet1)
                        childListDataFrame=pd.read_excel(path)
                        parentlistDataframe=list
                    elif 'child' in sheet :
                        sheet1=[sh for sh in excelSheetList if sheet.replace('child','parent')==sh][0]
                        path=PATH+pathname+"/{0}".format(sheet1)
                        parentlistDataframe=pd.read_excel(path)
                        print(sheet,"-------",sheet1)
                        childListDataFrame=list
                    finshed_task_sheets.append(sheet)
                    finshed_task_sheets.append(sheet1)
                    for i in range(len(parentlistDataframe)):
                        dic1={}
                        for k,v in parentlistDataframe.items():
                            dic1[k.lower()]=v[i]
                        parentList.append(dic1)
                    for i in range(len(childListDataFrame)):
                        dic1={}
                        for k,v in childListDataFrame.items():
                            dic1[k.lower()]=v[i]
                        childList.append(dic1)
                    updated=0
                    updatedlist=[]
                    for dic in parentList:
                        value=dic.get('apply_link')
                        if value==None or str(value).strip()=='' or str(value).lower().strip()=="null":
                            del dic
                    for cdata in childList:
                        for pdata in parentList:
                            if fuzz.ratio(str(pdata.get('apply_link')).replace('s:',':').lower(),str(cdata.get('apply_link')).replace('s:',':').lower())>95:
                                for key in ['job_type','job_location','posted_date','functional_area','job_id']:
                                    if pdata.get(key)!=None and cdata.get(key)==None:
                                        cdata[key]=pdata.get(key)
                                if cdata.get('job_location')==None:
                                    for key in ['city','state','country']:
                                        print(cdata.get('job_location'),'  ',key)
                                        if pdata.get(key)!=None and str(pdata.get(key)).strip()!='' and str(pdata.get(key)).strip()!='nan' and str(pdata.get(key)).lower()!='null':
                                            if cdata.get('job_location')==None and cdata.get('pin')==None :
                                                cdata['job_location']=pdata.get(key)
                                            else:
                                                cdata['job_location']=cdata.get('job_location')+" "+str(pdata.get(key))
                                if cdata.get('pin')==None:
                                    if pdata.get('pin')!=None:
                                        cdata['pin']=pdata.get('pin')
                                break
                            elif pdata.get('job_title')!=None and  pdata.get('job_id')!=None:
                                if str(pdata.get('job_id')).strip()==str(cdata.get('job_id')).strip() :
                                    for key in ['job_type','job_location','posted_date','functional_area','job_id']:
                                        if pdata.get(key)!=None and cdata.get(key)==None:
                                            cdata[key]=pdata.get(key)
                                    if cdata.get('job_location')==None:
                                        for key in ['city','state','country']:
                                            if pdata.get(key)!=None and str(pdata.get(key)).strip()!='' and str(pdata.get(key)).strip()!='nan' and str(pdata.get(key)).lower()!='null':
                                                if cdata.get('job_location')==None and cdata.get('pin')==None :
                                                    cdata['job_location']=pdata.get(key)
                                                else:
                                                    cdata['job_location']=cdata.get('job_location')+" "+pdata.get(key)
                                    if cdata.get('pin')==None:
                                        if pdata.get('pin')!=None:
                                            cdata['pin']=pdata.get('pin')
                                    break

                    joblist=childList
            else:
                continue
            if len(joblist)==0:
                for i in range(len(list)):
                    dic1={}
                    for k,v in list.items():
                        dic1[k.lower()]=v[i]
                    joblist.append(dic1)
            responses=[]
            dic={}
            for job in joblist:
                job['scrappedby']=pathname
                job['tested_status']='False'
                job['company_info_id']=int(job.get('company_info_id'))
                for key,value in job.items():
                    if str(value).lower().strip()!='nan':
                        dic[key]=value
                job=dic        
                try:
                    if job.get('job_id')!=None:
                        job['job_id']=int(job.get('job_id'))
                except:
                    pass
                request_data=storeJob_request(job)
                if request_data.get('error')==None and request_data.get('detail')==None:
                    if request_data.get('status')=='succses':
                        inserted_database_rows_count+=1
                    elif request_data.get('duplicateEntry')!=None:
                        duplicate_job_rows+=1
                else:
                    error_rows_count+=1
                    error_rows.append(request_data)
        return JsonResponse({'companies':companies,'duplicate_job_rows_count':duplicate_job_rows,'error_count':error_rows_count,"inserted_database_rows_count":inserted_database_rows_count,'error_rows':str(error_rows).replace("'",' ')})
def storeJob_request(job):
    try:
        job_post_request=requests.post("http://"+str(socket.gethostbyname(socket.gethostname()))+':3000/get_data/',data=json.dumps(job))
    except Exception as exc:
        print("StoreJobsRestservice Got connection Exception",str(exc))
        print("trying after 2 minute.......")
        time.sleep(120)
        try:
            return storeJob_request(job)
        except:
            print("trying after 2 minute.......")
            time.sleep(120)
            return  storeJob_request(job)
    if job_post_request.status_code>=400 and job_post_request.status_code<500:
        time.sleep(120)
        print("StoreJob_request got 400 trying after 2 minutes")
        return storeJob_request(job)
    if  job_post_request.status_code>=500 and job_post_request.status_code<600:
        print("StoreJobsRestservice Got exception")
        return job_post_request.json()
    if job_post_request.status_code==201:
        return job_post_request.json()
    elif job_post_request.status_code==205:
        return {'error':job_post_request.json()}
    else:
        return job_post_request.json()


def refineColumns(job):
    new_jobData={}
    for key,value in job.items():
        if value!=None:
            if key.lower()=="posted_date":
                print(True)
                try:
                    date=validatos(value)
                except ValueError:
                    pass
                new_jobData[key.lower()]=date
                continue
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
def HtmlParser(data,info_id,job):
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
        for item in ['Deadline','Salary','Deadline:','Salary:','location:','locations:','work location(s):','team:', 'reports to:','title:','hours:','pay rate:','Req. ID:','Recruiter:','Role:','Position Location:','Reports To:','Allocation Specialist','Business Unit:','Supervision:','Supervision:','Full Time, Fixed Term - 12 Months','Requisition ID:','Position Title:','Project:','Relocation Authorized:','Position to be Panel Interviewed?','Grade:','Work Authorization:','Other Requirements:','Company:','Req ID:','Date:','Start Date:','Work type:','Categories:','Job no:','Contract:','Profile :','Scope :','POSITION:','DEPARTMENT:','BASE RATE OF PAY:','SHIFT:','Your future manager :','Scope :','Reporting Relationship']:
           if item.lower().strip() in x.getText().strip().lower():
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

def sheets_checking(request,pathname):
    excelSheetList=os.listdir(PATH+pathname)
    joblist=[]
    parentlistDataframe=None
    childListDataFrame=None
    parentList=None
    childList=None
    finshed_task_sheets=[]
    companies=0
    for sheet in excelSheetList:
        companies+=1
        path=PATH+pathname+"/{0}".format(sheet)
        list=pd.read_excel(path)
        if sheet not in finshed_task_sheets:
            if 'parent' in sheet or 'child'in sheet:
                if 'parent' in sheet:
                    sheet1=[sh for sh in excelSheetList if sheet.replace('parent','child')==sh][0]
                    path=PATH+pathname+"/{0}".format(sheet1)
                    childListDataFrame=pd.read_excel(path)
                    parentlistDataframe=list
                elif 'child' in sheet:
                    sheet1=[sh for sh in excelSheetList if sheet.replace('child','parent')==sh][0]
                    path=PATH+pathname+"/{0}".format(sheet1)
                    parentlistDataframe=pd.read_excel(path)
                    childListDataFrame=list
                finshed_task_sheets.append(sheet)
                finshed_task_sheets.append(sheet1)
    return JsonResponse({'json':True})
def identifying_location_with_postalcode(pin):
    location=StoreLocation.objects.filter(postal_code=pin)
    if len(location)!=0:
        job_location=location[0].city+", "+location[0].state_code
        country_type=location[0].country_code
        return {'job_location':job_location,'country_type':country_type,'scrapped_location':pin}
    else:
        return 0

class ApiData(View):
    def get(self,request,*args,**kwrgs):
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        token=generateToken()
        jobscount=0
        dupli=0
        erro=[]
        pjobsperc=[]
        cjobsperc=None
        cid=request.GET.get('cid')
        pid=request.GET.get('pid')
        types=request.GET.get('type')
        if types==None:
            raise TypeError()
        if pid !=None:
            param={ 'Authorization':'bearer {0}'.format(token)}
            pjobsperc=[]
            offset=0
            while True:
                url='''https://advancedapi.octoparse.com/api/notexportdata/gettop?taskId={0}&size=1000'''.format(pid)
                param={ 'Authorization':'bearer {0}'.format(token)}
                apireq=requests.get(url,headers=param)
                if apireq.status_code==200:
                    jobsperc=apireq.json()
                    if jobsperc['data']['currentTotal']>0:
                        if len(jobsperc['data']['dataList'])==1000:
                            for x in jobsperc['data']['dataList']:
                                pjobsperc.append(x)
                            param={ 'Authorization':'bearer {0}'.format(token)}
                            url='''https://advancedapi.octoparse.com/api/notexportdata/update?taskId={0}'''.format(pid)
                            apireq=requests.post(url,headers=param)
                            continue
                        else:
                            if jobsperc['data']['currentTotal']>0:
                                for x in jobsperc['data']['dataList']:
                                    pjobsperc.append(x)
                                break
        offset=0
        cjobsperc=[]
        while True:
            url='''https://advancedapi.octoparse.com/api/notexportdata/gettop?taskId={0}&size=1000'''.format(cid)
            param={ 'Authorization':'bearer {0}'.format(token)}
            apireq=requests.get(url,headers=param)
            if apireq.status_code==200:
                jobsperc=apireq.json()
                if jobsperc['data']['currentTotal']>0:
                    if len(jobsperc['data']['dataList'])==1000:
                        for x in jobsperc['data']['dataList']:
                            cjobsperc.append(x)
                        param={ 'Authorization':'bearer {0}'.format(token)}
                        url='''https://advancedapi.octoparse.com/api/notexportdata/update?taskId={0}'''.format(cid)
                        apireq=requests.post(url,headers=param)
                        continue
                    else:
                        if jobsperc['data']['currentTotal']>0:
                            for x in jobsperc['data']['dataList']:
                                cjobsperc.append(x)
                            break
            if apireq.status_code==401 or apireq.status_code==402 :
                erro.append(list)
        jobs=[]
        c=0
        t=0
        if pid!=None:
            for cdata in cjobsperc:
                for pdata in pjobsperc:
                    if cdata.get('apply_link')==pdata.get('apply_link'):
                        c+=1
                    if pdata.get('job_title')==cdata.get('job_title') and pdata.get('apply_link')==cdata.get('apply_link') :
                        t+=1
                        if cdata.get('job_id')==None or cdata.get('job_id')=='' :
                            if pdata.get('job_id')!=None:
                                cdata['job_id']=pdata['job_id']
                        if cdata.get('posted_date')==None or cdata.get('posted_date')=='' :
                            if pdata.get('posted_date')!=None:
                                cdata['posted_date']=pdata['posted_date']
                        if cdata.get('job_location')==None or cdata.get('job_location')=='' :
                            if pdata.get('job_location')!=None:
                                cdata['job_location']=pdata['job_location']
                        if cdata.get('job_title')==None or cdata.get('job_title')=='' :
                            if pdata.get('job_title')!=None:
                                cdata['job_title']=pdata['job_title']
                        if cdata.get('job_location')==None or cdata.get('job_location')=='' :
                            if pdata.get('job_location')!=None:
                                cdata['job_location']=pdata['job_location']
                        if cdata.get('job_type')==None or cdata.get('job_type')=='' :
                            if pdata.get('job_type')!=None:
                                cdata['job_type']=pdata['job_type']
                        break
                jobs.append(cdata)
        else:
            for cdata in cjobsperc:
                jobs.append(cdata)
        plen=0
        if pjobsperc!=None:
            plen=len(pjobsperc)
        clen=len(cjobsperc)
        job['company_info_id']=int(job['company_info_id'])
        try:
            job['job_id']=int(job['job_id'])
        except:
            pass
        for job in jobs:
            dic1={}
            dic1=dict((k.lower(),v) for k,v in job.items())
            job=dataModify(**dic1)
            if types=="ini" or types=="INI":
                dup=web_internship_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],posted_date=job['posted_date'])
                if len(dup)!=0:
                    dupli+=1
                else:
                    com=web_internship_jobs(**job)
                    com.save()
                    jobscount+=1
            elif types=='com' or types=='COM':
                dup=company_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],posted_date=job['posted_date'])
                if len(dup)!=0:
                    dupli+=1
                else:
                    com=company_jobs(**job)
                    com.save()
                    jobscount+=1
        return JsonResponse({'data':{'request':'succsess','duplicates':dupli,'parentLength':plen,'childLength':clen,'jobs':jobscount,'errors':erro},'anotherLanguagesJobs_data':anotherLanguagesJobs_data})
def generateToken():
    body={"username":"software@gradsiren.com","password":"reset#123","grant_type":"password"}
    apireq=requests.post('https://advancedapi.octoparse.com/token',body)
    return apireq.json()['access_token']
class VaultData(View):
    def get(self,request,*args,**kwrgs):
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        type=request.GET.get('type')
        companies=0
        jobs=0
        dupli=0
        excelSheetList=os.listdir(r'C:\Users\Emphyd12146rjee1\Desktop\excelsheet data gettin\sheets')
        joblist=[]

        for sheet in excelSheetList:
            companies+=1
            sheetdata=[]
            path=r"C:\Users\Emphyd12146rjee1\Desktop\excelsheet data gettin\sheets\{0}".format(sheet)
            list=pd.read_excel(path)
            if sheet=="vault-data-443-pages-company.xlsx":
                dict1=dict((k,str(v)) for k, v in dict(list['related_internship']).items())
            else:
                dict1=dict((k,str(v)) for k, v in dict(list['Internship_Name']).items())
            joblist.append(dict1)
        sheet1=joblist[1]
        sheet2=joblist[0]
        valid=0
        dupli=0
        with open('dupli.txt','a') as dump:
            for values1 in sheet1.values():
                yes=None
                for values2 in sheet2.values():
                    if  values2==values1:
                        print(values1,"------",values2)
                        yes="data"
                        dupli+=1
                        dump.write(values1+"\n")
                        break
                if yes==None:
                    valid+=1
                    validline=open('validLine.txt','a')
                    validline.write(str(values1)+"\n")
                    validline.close()
        print(len(sheet1))
        print(len(sheet2))
        return JsonResponse({"dupli":dupli,"valid":valid})

class Posted_dater(View):
    def get(requests,*args,**kwrgs):
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        count=0
        deletedCount=0
        changed=None
        deleted=None
        dataList=company_jobs.objects.all()
        print(len(dataList))
        for data in dataList:
            changed=None
            for x in company_jobs._meta.fields:
                print('started')
                dic={'col':str(x).replace('web.company_jobs.','')}
                if dic['col']=='job_description':
                    if str(data.__dict__[dic.get('col')]).strip()=='nan':
                        data.delete()
                        deleted="chenged"
                elif str(data.__dict__[dic.get('col')]).strip()=='nan':
                    data.__dict__[dic.get('col')]=None
                    changed="changed"
            if changed!=None:
                data.save()
                count+=1
            if deleted!=None:
                deletedCount+=1
        return JsonResponse({"modified_count":count,'delcount':deletedCount})
class Sheet_exception(Exception):
    pass
import requests
import json

from copy import copy


def searchLocationInDatabase(data):
    data=data.replace(',','-')
    data=data.replace('|','-')
    data=data.replace('||','-')
    return data
class DeleteModelObject(View):
    def get(self,request):
        auth=request.GET.get('auth')
        if auth==None:
            return JsonResponse({'status':'failed please provide authentication'})
        count=0
        startvalue=request.GET.get('start')
        endvalue=request.GET.get('end')
        if startvalue==None:
            return JsonResponse({'status':"failed please provide start value"})
        if endvalue==None:
            return JsonResponse({'status':"failed please provide end value"})
        for x in range(int(startvalue),int(endvalue)):
            print(count,x)
            data=web_internship_jobs.objects.filter(web_internship_jobs_id=x)
            if len(data)!=0:
                applyLink=str(data[0].apply_link)
                try:
                    reqdata=requests.get(applyLink)
                    if reqdata.status_code>=400 and reqdata.status_code<=499:
                        data.delete()
                        count+=1
                        orr=open('applyLinkdata','a')
                        orr.write(str(applyLink)+"------400\n")
                        orr.close()
                        continue
                except:
                    continue
                htmltext=text_from_html(reqdata.text)
                if 'invalid url' in str(htmltext).lower() or 'page not found' in str(htmltext).lower() or 'this job is expired' in str(htmltext).lower() or 'no longer available' in str(htmltext).lower() or 'job not found' in str(htmltext).lower() or  'has been removed' in str(htmltext).lower() or 'this job has either expired' in str(htmltext).lower() or 'been removed' in str(htmltext).lower() or 'job is closed' in str(htmltext).lower() or 'has been filled' in str(htmltext).lower() or 'Sorry! The job you are looking for is no longer' in str(htmltext).lower():
                    data.delete()
                    count+=1
                    orr=open('applyLinkdata','a')
                    orr.write(str(applyLink)+"-----page\n")
                    orr.close()
        return JsonResponse({'count':count})
import os
from django.http import Http404,HttpResponse
def filedownlod(request):
    filepath=DRIVE+r"\jeevan\django\excelsheetdatastore\media\Internships Catergories.xlsx"
    with open(filepath,'rb') as orr:
        respone=HttpResponse(orr.read(),content_type="application/.xlsx")
        respone['Content-Disposition']='inline; filename=' + filepath
    return respone
def refineJob_description(request):
    start=int(request.GET.get('start'))
    stop=int(request.GET.get('stop'))
    for x in range(start,stop):
        dataload=web_internship_jobs.objects.filter(web_internship_jobs_id=x)
        print(dataload)
        if len(dataload)!=0:
            soup=BeautifulSoup(dataload[0].job_description,"html.parser")
            data=soup.findAll()
            for tag in data:
                if len(tag.getText(strip=True))==0:
                    try:
                        if len(data[data.index(tag)+2].getText(strip=True))==0:
                            tag.extract()
                    except:
                        pass
            dataload[0].job_description=str(soup)
            dataload[0].save()
    return HttpResponse("succese")
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
    city=None
    state=None
    country_type=None
    for index in location:
        if state!=None and city!=None:
            break
        if len(index)==2:
            state_data=StoreLocation.objects.filter(state_code=index)
            if len(state_data)!=0:
                state=state_data[0].state_code
                continue
        if city==None:
            city_data=StoreLocation.objects.filter(city=index)
            if len(city_data)!=0:
                city=city_data[0].city
                continue
        if state==None:
            state_data=StoreLocation.objects.filter(state=index)
            if len(state_data)!=0:
                state=state_data[0].state_code
                continue
            if len(state_data)==0:
                state_data=StoreLocation.objects.filter(state=index)
                if len(state_data)!=0:
                    state=state_data[0].state_code
                    continue
    if city==None or state==None:
        return {'location':0}
    if city!=None and state!=None:
        country_type=StoreLocation.objects.filter(state_code=state,city=city)
        if len(country_type)!=0:
            country_type=country_type[0].country_code
            return {"location":{'city':city,'state_code':state,'country_type':country_type}}
        return {'location':0}
    return {'location':0}

def get_location_from_googleApi(location):
    city=None
    state_code=None
    country_type=None
    try:
        location_request=requests.get('http://api.geonames.org/searchJSON?q={location}&maxRows=20&username=optncpt'.format(location=location.replace('#','')))
    except:
        print("get_location_from_googleApi got Error So Sleeping for 20 secs")
        time.sleep(20)
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

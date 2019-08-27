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
# job={'job_location':'Agia Rd, Goalpara, Assam'}
# data=Instructions(31,job).method_caller()
# print(data)
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
DRIVE=config.get('DRIVE')

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
        job_errorList=[]
        job_errCount=0
        anotherLanguagesJobs=0
        anotherLanguagesJobs_data=[]
        closed_jobs_count=0
        closed_jobs=[]
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
                            if str(pdata.get('apply_link')).replace('s:',':')==str(cdata.get('apply_link')).replace('s:',':'):
                                for key in ['job_type','job_location','posted_date','functional_area','job_id']:
                                    if pdata.get(key)!=None and cdata.get(key)==None:
                                        cdata[key]=pdata.get(key)
                                if cdata['job_location']==None:
                                    for key in ['city','state','country']:
                                        if pdata.get(key)!=None:
                                            if cdata.get('job_location')==None:
                                                cdata['job_location']=pdata.get(key)
                                            else:
                                                cdata['job_location']=cdata.get('job_location')+" "+pdata.get(key)
                                break
                            elif pdata.get('job_title')!=None and  pdata.get('job_id')!=None:
                                if str(pdata.get('job_id')).strip()==str(cdata.get('job_id')).strip() :
                                    for key in ['job_type','job_location','posted_date','functional_area','job_id']:
                                        if pdata.get(key)!=None and cdata.get(key)==None:
                                            cdata[key]=pdata.get(key)
                                    if cdata['job_location']==None:
                                        for key in ['city','state','country']:
                                            if pdata.get(key)!=None:
                                                if cdata.get('job_location')==None:
                                                    cdata['job_location']=pdata.get(key)
                                                else:
                                                    cdata['job_location']=cdata.get('job_location')+" "+pdata.get(key)
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

            for dic in joblist:
                if dic.get('job_location')==None:
                    del dic
            for dic12 in joblist:
                dated={}
                if dic12.get('job_location')==None:
                    if dic12.get('city')!=None and  dic12.get('state')!=None:
                        if str(dic12.get('city')).strip()=='nan':
                            dic12['city']=''
                        if str(dic12.get('state')).strip()=='nan':
                            dic12['state']=''
                        dic12['job_location']=dic12.get('city')+" , "+dic12.get('state')
                        del dic12['city']
                        del dic12['state']
                if dic12.get('posted_date')!=None:
                    dated['scrapped_date']=dic12['posted_date']
                colmn=[]
                try:
                    checkJobs=dataModify(**dic12)
                except TypeError as exc:
                    columnnameErrorCount+=1
                    columnnameError.append({str(sheet):str(exc)})
                    if 'parent' in sheet or 'child' in sheet:
                        continue
                    break
                job=dic12
                if 'position has been closed' in str(job.get('job_description')).lower():
                    closed_jobs.append(job)
                    closed_jobs_count+=1
                    continue
                job['job_location']=str(job.get('job_location','')).replace('Various Locations','').replace('nan','')
                if job['job_description']==None or str(job['job_description'])=='nan' or str(job['job_description']).lower()=='null':
                    if (str(job.get('job_roles_responsibilities')).strip()=='nan' and str(job.get('qualifications')).strip()=='nan') or (str(job.get('job_roles_responsibilities')).strip()=='None' and str(job.get('qualifications')).strip()=='None') or (str(job.get('job_roles_responsibilities')).strip()=='' and str(job.get('qualifications')).strip()==''):
                        job_errCount+=1
                        job_errorList.append({'job_description':str(job)})
                        continue
                """
                Beautify the Data
                """
                Beautify_objects=Beautify_company_jobs.objects.filter(company_info_id=job['company_info_id'])
                if len(Beautify_objects)!=0:
                    for obj in Beautify_objects:
                        job =Instructions(obj.instruction_id,job).method_caller()
                for key,value in job.items():
                    if str(value).strip()=='' or str(value).strip()=="NULL" or str(value).strip()=="null" or str(value).strip()==str(float('nan')):
                        job[key]=None
                if job.get('posted_date')!=None:
                    if len(dated)!=0:
                        try:
                            dated['modified_date']=validatos(job['posted_date'])
                            datesList.append(dated)
                        except ValueError:
                            open_html=open(r'C:\sample.html','w')
                            data="<body><b>scrappedBy</b>:{scarpby}<br><b>{job_title}</b><br><b>{posted_date}</b><br><b>{excel}</b></body>".format(scarpby=pathname,job_title=job.get('job_title'),posted_date=job.get('posted_date'),excel=sheet)
                            open_html.write(data)
                            open_html.close()
                            webbrowser.open(r'C:\Users\Emphyd12146rjee1\Downloads\sample.html')
                            ExceptionList.append({'posted_date':job.get('posted_date')})
                            job['posted_date']=datetime.today().date()
                if job.get('job_id')!=None  and len(str(job.get('job_id')))>=75:
                    job['job_id']=None
                for key,value in job.items():
                    if str(value).strip()=='nan' or str(value).strip()=='' or value==None:
                        job[key.lower()]=None
                    else:
                        job[key.lower()]=str(value).strip()
                type=None
                for value in [job['job_title'],job.get('job_type'),job.get('functional_area')]:
                    value=str(value).strip()
                    if value!=None or value !='null' or value !="NULL" or str(value)!='nan' or value!='' :
                        if 'intern-' in [str(x).lower().strip() for x in value.split()] or 'intern' in [str(x).lower().strip() for x in value.split()] or 'intern.' in [str(x).lower().strip() for x in value.split()] or 'intern,' in [str(x).lower().strip() for x in value.split()] or 'intern ' in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                        if  'internship' in [str(x).lower().strip() for x in value.split()] or 'internship.' in [str(x).lower().strip() for x in value.split()] or 'internship,' in [str(x).lower().strip() for x in value.split()] or 'internship ' in [str(x).lower().strip() for x in value.split()] or 'internship' in [str(x).lower().strip() for x in value.split()] or 'internship' in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                        if 'fellowship' in [str(x).lower().strip() for x in value.split()] or 'fellowship.' in [str(x).lower().strip() for x in value.split()] or 'fellowship,' in [str(x).lower().strip() for x in value.split()] or 'fellowship' in [str(x).lower().strip() for x in value.split()] or 'fellowship' in [str(x).lower().strip() for x in value.split()] or 'fellowship' in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                        if 'aperentship'  in [str(x).lower().strip() for x in value.split()] or 'aperentship.'  in [str(x).lower().strip() for x in value.split()] or 'aperentship,'  in [str(x).lower().strip() for x in value.split()] or 'aperentship'  in [str(x).lower().strip() for x in value.split()] or 'aperentship'  in [str(x).lower().strip() for x in value.split()] or 'aperentship'  in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                        if 'trainee'  in [str(x).lower().strip() for x in value.split()] or 'trainee.'  in [str(x).lower().strip() for x in value.split()] or 'trainee,'  in [str(x).lower().strip() for x in value.split()] or 'trainee'  in [str(x).lower().strip() for x in value.split()] or 'trainee'  in [str(x).lower().strip() for x in value.split()] or 'trainee'  in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                        if 'apprenticeship'  in [str(x).lower().strip() for x in value.split()] or 'apprenticeship.'  in [str(x).lower().strip() for x in value.split()] or 'apprenticeship,'  in [str(x).lower().strip() for x in value.split()] or 'apprenticeship'  in [str(x).lower().strip() for x in value.split()] or 'apprenticeship'  in [str(x).lower().strip() for x in value.split()] or 'apprenticeship'  in [str(x).lower().strip() for x in value.split()]:
                            type="INI"
                            break
                job=refineColumns(job)
                if type==None:
                    type="com"
                if job.get('job_title')==None or str(job.get('job_title'))=='nan':
                    job_errCount+=1
                    job_errorList.append({'job_title':str(job)})
                    continue
                if job.get('job_description')==None or str(job.get('job_description'))=='nan' :
                    if (str(job.get('job_roles_responsibilities')).strip()=='nan' and str(job.get('qualifications')).strip()=='nan') or (str(job.get('job_roles_responsibilities')).strip()=='None' and str(job.get('qualifications')).strip()=='None') or (str(job.get('job_roles_responsibilities')).strip()=='' and str(job.get('qualifications')).strip()==''):
                        job_errCount+=1
                        job_errorList.append({'job_description':str(job)})
                        continue
                if job.get('job_location')==None or  str(job.get('job_location'))=='nan':
                    job_errCount+=1
                    job_errorList.append({'job_location':str(job)})
                    continue
                if job.get('company_name')==None:
                    job_errCount+=1
                    job_errorList.append({'company_name':str(job)})
                    continue
                if job.get('company_info_id')==None:
                    job_errCount+=1
                    job_errorList.append({'company_info_id':str(job)})
                    continue
                if job.get('apply_link')==None:
                    job_errCount+=1
                    job_errorList.append({'apply_link':str(job)})
                    continue
                info_id=job['company_info_id']
                for key,value in job.items():
                    if 'job_description' in key:
                        if job[key]!=None:
                            job[key]=HtmlParser(value,info_id,job)
                        else:
                            job[key]=value
                    if 'qualifications' in key:
                        if job[key]!=None:
                            job[key]=HtmlParser(value,info_id,job)
                        else:
                            job[key]=value
                    if 'job_roles_responsibilities' in key:
                        if job[key]!=None:
                            job[key]=HtmlParser(value,info_id,job)
                        else:
                            job[key]=value
                    if 'job_requirements' in key:
                        if job[key]!=None:
                            job[key]=HtmlParser(value,info_id,job)
                        else:
                            job[key]=value
                job['scrapped_date']=datetime.now()
                abborted=None
                job['scrappedBy']=pathname
                if job.get('posted_date')==None:
                    abborted="modified"
                    job['posted_date']=job['scrapped_date']
                if len(str(BeautifulSoup(str(job.get('job_description')),'html.parser').getText()).strip())==0:
                    if (str(job.get('job_roles_responsibilities')).strip()=='nan' and str(job.get('qualifications')).strip()=='nan') or (str(job.get('job_roles_responsibilities')).strip()=='None' and str(job.get('qualifications')).strip()=='None') or (str(job.get('job_roles_responsibilities')).strip()=='' and str(job.get('qualifications')).strip()==''):
                        job_errCount+=1
                        job_errorList.append({'job_description':str(job)})
                        continue
                if 'This job posting is only available in the language of the country where the position is located. Please refer to the corresponding language to initiate your application.' in str(job.get('job_description')) or 'This job posting is only available in German language' in str(job.get('job_description')):
                    job_errorList.append({"job_description":str(job)})
                    continue
                try:
                    for x in ['job_description','job_roles_responsibilities','qualifications']:
                        if str(job.get(x))!="None":
                            job[x]=re.sub('\s+',' ',str(job.get(x)))
                            language_detector=detect_langs(str(BeautifulSoup(job[x],'html.parser').get_text()))
                            break

                except:
                    anotherLanguagesJobs+=1
                    anotherLanguagesJobs_data.append({str(language_detector):str(job)})
                    continue
                if len(language_detector)>1:
                    anotherLanguagesJobs_data.append({str(language_detector):str(job)})
                    anotherLanguagesJobs+=1
                    continue
                else:
                    content_spliter=str(language_detector[0]).split(':')
                    if content_spliter[0]=='en':
                        if '0.9999' not in content_spliter[1]:
                            anotherLanguagesJobs+=1
                            anotherLanguagesJobs_data.append({str(language_detector):str(job)})
                            continue
                    else:
                        anotherLanguagesJobs+=1
                        anotherLanguagesJobs_data.append({str(language_detector):str(job)})
                        continue

                if 'remote'!=job['job_location'].lower().strip():
                    job.update(locationIdentifier(job['job_location'].replace('Headquarters','').replace('Various Locations','').replace('Airport','').replace('school','')))
                job['company_info_id']=int(float(job['company_info_id']))
                if job.get('other_locations')!=None:
                    job['other_locations']=job.get('other_locations').replace(job.get('job_location'),'')
                if job.get('job_id')!=None:
                    try:
                        job['job_id']=int(float(job.get('job_id')))
                    except:
                        pass
                if job.get('job_location')!=None and job.get('other_locations')!=None:
                    job['other_locations']=job.get('other_locations').replace(job.get('job_location'),'')
                if 'taleo' in job.get('apply_link'):
                    if '?' not in job.get('apply_link'):
                        job['apply_link']=job.get('apply_link')+"?job="+str(job.get('job_id'))
                    else:
                        job['apply_link']=job.get('apply_link')+"&job="+str(job.get('job_id'))
                if type=='ini' or type=='INI':
                    if abborted==None:
                        dup=web_internship_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],posted_date=job.get('posted_date'),job_id=job.get('job_id'))
                    else:
                        dup=web_internship_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'))
                    if len(dup)!=0:
                        internsdupli+=1
                        print("requirment already satisfied",job.get('job_title'),"---",sheet,"----Interhsips")
                    else:
                        try:
                            com=web_internship_jobs(**job)
                            com.save()
                            print("---------sucesses-----",job.get('job_title'),"---",sheet,"----Interhsips")
                            interns+=1
                        except:
                            ExceptionList.append({'error':str(job)})
                            continue

                if type=='COM' or type=='com':
                    if abborted==None:
                        dup=company_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],posted_date=job.get('posted_date'),job_id=job.get('job_id'))
                    else:
                        dup=company_jobs.objects.filter(company_name=job['company_name'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'))
                    if len(dup)!=0:
                        jobsdupli+=1
                        print("requirment already satisfied",job.get('job_title'),"---",sheet,"----jobs")
                    else:
                        try:
                            com=company_jobs(**job)
                            com.save()
                            print("---------sucesses-----",job.get('job_title'),"---",sheet,"----jobs")
                            jobs+=1
                        except:
                            ExceptionList.append({'error':str(job)})
                            continue

        return JsonResponse({"jobs":str(jobs),'Interns':str(interns),"Jobsduplicates":str(jobsdupli),"internship Duplicates":str(internsdupli),"companies":str(companies),"dates":datesList,'Exception':job_errorList,'columnnameError':columnnameError,'updatedParentchildCount':str(updated),"Non-English_language_jobs_count":str(anotherLanguagesJobs),'ExceptionList':ExceptionList,'anotherLanguagesJobs_data':anotherLanguagesJobs_data,'closed_jobs_count':closed_jobs_count,'closed_jobs':closed_jobs})
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
        if 'location:' in   x.get_text().strip().lower() or 'locations:' in   x.get_text().strip().lower() or 'work location(s):' in   x.get_text().strip().lower() or 'team:' in   x.get_text().strip().lower() or 'reports to:'  in   x.get_text().strip().lower() or 'title:'  in   x.get_text().strip().lower() or 'hours:'  in   x.get_text().strip().lower() or 'pay rate:'  in   x.get_text().strip().lower() or 'Req. ID:'  in   x.get_text().strip() or 'Recruiter:'  in   x.get_text().strip():
            if x.parent!=None and len(x.parent.get_text().strip())<=70:
                x.parent.decompose()
            else:
                if len(x.get_text().strip())<=100:
                    x.decompose()
    soup=str(soup).replace('&#8203','').replace('Duties: JOB DESCRIPTION','')
    return replacer(str(soup))

def sheets_checking(request,pathname):
    excelSheetList=os.listdir(PATH'+pathname)
    joblist=[]
    parentlistDataframe=None
    childListDataFrame=None
    parentList=None
    childList=None
    finshed_task_sheets=[]
    companies=0
    for sheet in excelSheetList:
        companies+=1
        path=PATH'+pathname+"/{0}".format(sheet)
        list=pd.read_excel(path)
        if sheet not in finshed_task_sheets:
            if 'parent' in sheet or 'child'in sheet:
                if 'parent' in sheet:
                    sheet1=[sh for sh in excelSheetList if sheet.replace('parent','child')==sh][0]
                    path=PATH'+pathname+"/{0}".format(sheet1)
                    childListDataFrame=pd.read_excel(path)
                    parentlistDataframe=list
                elif 'child' in sheet:
                    sheet1=[sh for sh in excelSheetList if sheet.replace('child','parent')==sh][0]
                    path=PATH'+pathname+"/{0}".format(sheet1)
                    parentlistDataframe=pd.read_excel(path)
                    childListDataFrame=list
                finshed_task_sheets.append(sheet)
                finshed_task_sheets.append(sheet1)
    return JsonResponse({'json':True})

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

from django.shortcuts import render
from locationModifier.models import *
from django.views import View
from django.http import JsonResponse
import socket
from django.core import serializers
from random import shuffle
import json
import os
import re
from .extras import *
from .forms import UploadFiles
from django.db.models import  Count
from datetime import  datetime
from dateutil import parser
import requests
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from rest_framework import generics
from rest_framework import pagination
from locationModifier.serializers import *
import threading
import time
import configparser
from django.db.models import Q
Config = configparser.RawConfigParser()
data='configuration.ini'
Config.read(data)
config={}
for each_sec in Config.sections():
    config=dict((k, v) for k, v in  Config.items(each_sec))
PATH=config.get('allpath')
DRIVE=config.get('drive')
class GetJobs(generics.ListAPIView):
    serializer_class=WebCompanyJobsserializer
    def get_queryset(self):
        query = {}
        data = self.request.GET
        if data.get('skill')!=None:
            return Web_company_jobs.objects.filter(Q(company_name=data.get('skill')) |  Q(job_title__icontains=data.get('skill')) | Q(job_description=data.get('skill'))| Q(posted_date__range=[str(datetime.datetime.now()-datetime.timedelta(days=30)),str(datetime.datetime.now())]))[0:10]
        else:
            return []
    def get(self,request):
        return self.list(request)

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

class GetCompanyName(View):
    def get(self,request):
        companyname=request.GET.get('cname')
        try:
            data=int(companyname)
            data=company_infoCopy.objects.filter(company_info_id=data)
            x=data[0]
            list=[]
            page=request.GET.get('pg')
            val=int(request.GET.get('val'))
            jobs_idsAndInternNames=[]
            jobs_idsAndCompanyNames=[]
            if val==1:
                INterndata=Web_internships_jobs.objects.filter(company_info_id=x.company_info_id)
                if len(INterndata)!=0:
                    for jobsdata in INterndata[0:250:]:
                        jobs_idsAndInternNames.append({'type':"INI",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_internship_jobs_id),'job_id':jobsdata.web_internship_jobs_id})
                shuffle(jobs_idsAndInternNames)
                list.append({'company_info_id':x.company_info_id,'company_name':x.company_name,"jobsdata":jobs_idsAndInternNames[0:30:]})
                return JsonResponse({'status':'success','data':list,'page':page,"pageNation":"page","showmin":page+"1",'showmax':int(page+"1")+len(list)-1,"max":len(data)})
            elif val==2:
                CompanyJObsdata=Web_company_jobs.objects.filter(company_info_id=x.company_info_id)
                if len(CompanyJObsdata)!=0:
                    for jobsdata in CompanyJObsdata[0:250:]:
                        jobs_idsAndCompanyNames.append({'type':"COM",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_company_jobs_id),'job_id':jobsdata.web_company_jobs_id})
                shuffle(jobs_idsAndCompanyNames)
                list.append({'company_info_id':x.company_info_id,'company_name':x.company_name,"jobsdata":jobs_idsAndCompanyNames[0:30:]})
                return JsonResponse({'status':'success','data':list,'page':page,"pageNation":"page","showmin":page+"1",'showmax':int(page+"1")+len(list)-1,"max":len(data)})
        except ValueError:
            data=None
        page=request.GET.get('pg')
        val=int(request.GET.get('val'))
        if data==None:
            if val==2:
                data=company_infoCopy.objects.filter(company_name=companyname)
            if len(data)==0:
                if val==2:
                    data=company_infoCopy.objects.filter(company_name__icontains=companyname)
        list=[]
        if len(data)!=0 and len(data)<=10:
            if val==2:
                for x in data:
                    jobs_idsAndCompanyNames=[]
                    INterndata=Web_internships_jobs.objects.filter(company_info_id=x.company_info_id)
                    if len(INterndata)!=0:
                        for jobsdata in INterndata[0:250:]:
                            jobs_idsAndCompanyNames.append({'type':"INI",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_internship_jobs_id),'job_id':jobsdata.web_internship_jobs_id})
                    else:
                        CompanyJObsdata=Web_company_jobs.objects.filter(company_info_id=x.company_info_id)
                        if len(CompanyJObsdata)!=0:
                            for jobsdata in CompanyJObsdata[0:250:]:
                                jobs_idsAndCompanyNames.append({'type':"COM",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_company_jobs_id),'job_id':jobsdata.web_company_jobs_id})
                    shuffle(jobs_idsAndCompanyNames)
                    list.append({'company_info_id':x.company_info_id,'company_name':x.company_name,"jobsdata":jobs_idsAndCompanyNames[0:30:]})
            if val==1:
                for x in data:
                    jobs_idsAndCompanyNames=[]
                    INterndata=Web_internships_jobs.objects.filter(company_info_id=x.company_info_company_info_id)
                    if len(INterndata)!=0:
                        for jobsdata in INterndata[0:250:]:
                            jobs_idsAndCompanyNames.append({'type':"INI",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_internship_jobs_id),'job_id':jobsdata.web_internship_jobs_id})
                    else:
                        CompanyJObsdata=Web_company_jobs.objects.filter(company_info_id=x.company_info_company_info_id)
                        if len(CompanyJObsdata)!=0:
                            for jobsdata in CompanyJObsdata[0:250:]:
                                jobs_idsAndCompanyNames.append({'type':"COM",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_company_jobs_id),'job_id':jobsdata.web_company_jobs_id})
                    shuffle(jobs_idsAndCompanyNames)
                    list.append({'company_info_id':x.company_info_company_info_id,'company_name':x.company_name,"jobsdata":jobs_idsAndCompanyNames[0:30:]})
            return JsonResponse({'status':'success','data':list,"pageNation":"pageNation","showmin":0,"showmax":len(list),"max":len(data)})
        if len(data)>10:
            max=int(page+"1")+10
            min=int(page+"0")
            if max >= len(data):
                max=len(data)
            if val==2:
                for x in range(min,max):
                    jobs_idsAndCompanyNames=[]
                    INterndata=Web_internships_jobs.objects.filter(company_info_id=data[x].company_info_id)
                    if len(INterndata)!=0:
                        for jobsdata in INterndata[0:250:]:
                            jobs_idsAndCompanyNames.append({'type':"INI",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_internship_jobs_id),'job_id':jobsdata.web_internship_jobs_id})
                    else:
                        CompanyJObsdata=Web_company_jobs.objects.filter(company_info_id=data[x].company_info_id)
                        if len(CompanyJObsdata)!=0:
                            for jobsdata in CompanyJObsdata[0:250:]:
                                jobs_idsAndCompanyNames.append({'type':"COM",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_company_jobs_id),'job_id':jobsdata.web_company_jobs_id})
                    shuffle(jobs_idsAndCompanyNames)
                    list.append({'company_info_id':data[x].company_info_id,'company_name':data[x].company_name,"jobsdata":jobs_idsAndCompanyNames[0:30:]})

            if val==1:
                for x in range(min,max):
                    jobs_idsAndCompanyNames=[]
                    INterndata=Web_internships_jobs.objects.filter(company_info_id=data[x].company_info_company_info_id)
                    if len(INterndata)!=0:
                        for jobsdata in INterndata[0:250:]:
                            jobs_idsAndCompanyNames.append({'type':"INI",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_internship_jobs_id),'job_id':jobsdata.web_internship_jobs_id})
                    else:
                        CompanyJObsdata=Web_company_jobs.objects.filter(company_info_id=data[x].company_info_company_info_id)
                        if len(CompanyJObsdata)!=0:
                            for jobsdata in CompanyJObsdata[0:250:]:
                                jobs_idsAndCompanyNames.append({'type':"COM",'job_title':str(jobsdata.job_title)+"-------"+str(jobsdata.web_company_jobs_id),'job_id':jobsdata.web_company_jobs_id})
                    shuffle(jobs_idsAndCompanyNames)
                    list.append({'company_info_id':data[x].company_info_company_info_id,'company_name':data[x].company_name,"jobsdata":jobs_idsAndCompanyNames[0:30:]})


        return JsonResponse({'status':'success','data':list,'page':page,"pageNation":"page","showmin":page+"1",'showmax':int(page+"1")+len(list)-1,"max":len(data)})
from copy import deepcopy
def gethtml(request):
    ip=str(socket.gethostbyname(socket.gethostname()))
    internLIST=os.listdir(PATH)
    dataList=[]
    internLISTCopy=deepcopy(internLIST)
    for x in internLIST:
        list=os.listdir(PATH+x)
        if len(list)==0:
            internLISTCopy.remove(x)
        if len(list)!=0:
            dataList.append({x:list})
    return render(request,'Home.html',{'data':ip,'dataLIST':dataList,"INTERNS":internLISTCopy})
from django.core import serializers
import json
def getCompanyData(request):
    cid=request.GET.get('cinfoid')
    if cid==None:
        return JsonResponse({"status":"failed","error":"please provide id"})
    dataList=company_infoCopy.objects.filter(company_info_id=cid)
    if len(dataList)!=0 and len(dataList)<=10:
        data=serializers.serialize('json',dataList)
        data=json.loads(data)
        if data[0]['fields'].get('hq_locations_location_id')!=None or data[0]['fields'].get('hq_locations_location_id')!='NULL':
            obj=Locations.objects.get(location_id=data[0]['fields'].get('hq_locations_location_id'))
            data[0]['fields']['hq_locations_location_id']=" ".join( x for x in [obj.city,obj.state_code,obj.postal_code])
        return JsonResponse(data[0]["fields"])

    return JsonResponse({"status":"success","error":"sorry doesn't have any data with this id".format(cid)})
from django.core.mail import send_mail
import datetime

def jeevan():
    ip=None
    oldip=None
    try:
        ip=str(socket.gethostbyname(socket.gethostname()))
        with open(DRIVE+r'ip.txt','r') as orr:
            oldip=str(orr.readline())
        if ip.strip()!=oldip.strip():
            send_mail_to_interns(ip)
    except:
        send_mail_to_interns(ip)
def send_mail_to_interns(ip):
    time=datetime.datetime.today()
    print("ip is changed sending Email......to Interns")
    body="Hello Interns\nIMP NOTE:- EVERYTIME DONT FORGET TO ALLOW NOTOFIACTIONS IN MOZILLA WHEN IP CHANGED\n For Getting Company Info id Ip is changed...at {time}\n Use this New url http://{ip}:7000/Home/   \n showing Bugs http://{ip}:7000/showbugs/ \n Please Use this urls in Mozila Browser\n IMP NOTE:- EVERYTIME DONT FORGET TO ALLOW NOTOFIACTIONS IN MOZILLA WHEN IP CHANGED\n                             Thank you".format(ip=ip,time=time)
    send_mail('Ip is Changed',body , 'rayalajeevan@gmail.com', ['jeevan.rayala@cogentdatasolutions.in',
        'anusha.upputholla@cogentdatasolutions.in',
        
        'santhialapati6@gmail.com',
        'ravalim03@gmail.com',
        'madhu21897@gmail.com',
        'katkamrohit11@gmail.com',
        'devaki.sowmya@gmail.com',
        'doolamravali432@gmail.com',])
    with open(DRIVE+'ip.txt','w') as orr:
        orr.write(ip)
try:
    jeevan()
except Exception as e:
     print(e)
     print("Internet Is not available Please send Manually.....!",str(e))
def renderHtml(request):
    jobid=request.GET.get('id')
    type=request.GET.get('type')
    htmlcode="""<html>
<link rel="icon" type="image/web-scraping-itsys.png" href="http://blog.website-scraping.com/wp-content/uploads/web-scraping-itsys.png"> 
<title>View Job</title>
<style>
    .iCIMS_JobOptions {
  display:none;}
    dl {
    font-size: 15px;
    font-weight: 400;
    color: #333;
    list-style-type: disc;
    padding-inline-start: 30px;
    }
    dl dt {
    display: list-item;
    text-align: -webkit-match-parent;
    list-style: disc;
    font-weight: 500;
    }
    ul {
    display: block;
    list-style-type: disc;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    padding-inline-start: 30px;
    }
    ul li {
    display: list-item;
    text-align: -webkit-match-parent;
    list-style: disc;
    margin: 10px 0;
    line-height: 20px;
    }
    ul ul {
    list-style-type: circle;
    }
    .newLine {
display: inline-grid;
font-weight: 600 !important;
margin-top: 20px;
font-family: "Segoe UI", sans-serif !important;
}
    }</style><body>"""
    if type=="INI":
        interndata=Web_internships_jobs.objects.filter(web_internship_jobs_id=int(jobid))
        if len(interndata)!=0:
            serlized_data=serializers.serialize('json',interndata)
            serlized_data=json.loads(serlized_data)
            for key,value in serlized_data[0]['fields'].items():
                if value!=None:
                    if key!='web_internship_jobs_id' :
                        if key=='apply_link':
                            htmlcode=htmlcode+"<a href='{}'>CLICK HERE TO APPLY</a>".format(str(value))
                            continue
                        elif key=='job_description':
                            htmlcode=htmlcode+"<h5><b>"+ key +": </b></h5><div class='job_description'>"+str(value)+"</div>"
                            continue
                        htmlcode=htmlcode+"<h5><b>"+ key +": </b></h5>"+str(value)
            htmlcode=htmlcode+"</body></html>"
    else:
        interndata=Web_company_jobs.objects.filter(web_company_jobs_id=int(jobid))
        if len(interndata)!=0:
            serlized_data=serializers.serialize('json',interndata)
            serlized_data=json.loads(serlized_data)
            for key,value in serlized_data[0]['fields'].items():
                if value!=None:
                    if key!='web_internship_jobs_id':
                        if key=='apply_link':
                            htmlcode=htmlcode+"<a href='{}'>CLICK HERE TO APPLY</a>".format(str(value))
                            continue
                        elif key=='job_description':
                            htmlcode=htmlcode+"<h5><b>"+ key +": </b></h5><div class='job_description'>"+str(value)+"</div>"
                            continue
                        htmlcode=htmlcode+"<h5><b>"+ key +": </b></h5>"+str(value)
            htmlcode=htmlcode+"</body></html>"
    return HttpResponse(htmlcode)
def Fileuploader(request):
    xceldata=request.FILES.getlist('upload')
    pathname=request.POST['uploadIntern']

    for excelsheets in xceldata:
        path=PATH+pathname+"/"+excelsheets.name
        fileread=open(path,'wb+')
        for chunk in excelsheets.chunks():
            fileread.write(chunk)
        fileread.close()
    internLIST=os.listdir(PATH)
    dataList=[]
    internLISTCopy=deepcopy(internLIST)
    for x in internLIST:
        list=os.listdir(PATH+x)
        if len(list)==0:
            internLISTCopy.remove(x)
        if len(list)!=0:
            dataList.append({x:list})
    return render(request,"Home.html",{'upload_status':"succsess",'dataLIST':dataList,"INTERNS":internLISTCopy})
def deleteExcelSheets(request):
    pathname=request.GET.get('fname')
    excelList=os.listdir(PATH+pathname)
    if len(excelList)!=0:
        for excel in excelList:
            os.remove(PATH+pathname+'/'+excel)
    internLIST=os.listdir(PATH)
    dataList=[]
    internLISTCopy=deepcopy(internLIST)
    for x in internLIST:
        list=os.listdir(PATH+x)
        if len(list)==0:
            internLISTCopy.remove(x)
        if len(list)!=0:
            dataList.append({x:list})
    return render(request,"Home.html",{'delete_status':"success",'dataLIST':dataList,"INTERNS":internLISTCopy})
def viewfiles(request):
    internLIST=os.listdir(PATH)
    dataList=[]
    for x in internLIST:
        list=os.listdir(PATH+x)
        if len(list)==0:
            internLIST.remove(x)
        else:
            dataList.append({x:list})
    return JsonResponse({'data':dataList,'INTERNS':internLIST})

class ViewJobsCOuntBYFilter(generics.ListAPIView):
    serializer_class=WebCompanyCOUNTJobsserializer
    pagination_class=StandardResultsSetPagination
    def get_queryset(self):
        data=dict((k,v[0]) for k,v in dict(self.request.GET).items() if k!='page' and str(v).strip()!='')
        if data:
            if data.get('company_info_id')!=None:
                datalist=Web_company_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter(company_info_id=data.get('company_info_id'))
                return datalist
            datalist=Web_company_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter(**data)
            return datalist
        return Web_company_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter()

    def get(self,request,*args,**kwrgs):
        return self.list(request)
class ViewInternsCOuntBYFilter(generics.ListAPIView):
    serializer_class=WebInternshipsCOUNTJobsserializer
    pagination_class=StandardResultsSetPagination
    def get_queryset(self):
        data=dict((k,v[0]) for k,v in dict(self.request.GET).items() if k!='page')
        if data:
            if data.get('company_info_id')!=None:
                return Web_internships_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter(company_info_id=data.get('company_info_id'))
            return Web_internships_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter(**data)
        return Web_internships_jobs_forSerlize.objects.values('company_info_id','tested_status','scrappedBy','company_name').annotate(dcount=Count('company_info_id')).filter()
        return []
    def get(self,request,*args,**kwrgs):
        return self.list(request)

def ViewJobsCount(request):
    return  render(request,"JobsDashBoard.html")
ip = str(socket.gethostbyname(socket.gethostname()))
def ViewJobsBydate(getdate,scrappedBy=None):
    dataList = []
    ip = str(socket.gethostbyname(socket.gethostname()))
    date= datetime.datetime.date(datetime.datetime.today())
    if "-" not  in getdate:
        date= datetime.datetime.date(datetime.datetime.today())
        if scrappedBy==None:
            data=Web_company_jobs.objects.values('company_info_id').annotate(dcount=Count('company_info_id')).filter(scrapped_date__icontains=date)
        else:
            data = Web_company_jobs.objects.values('company_info_id').annotate(dcount=Count('company_info_id')).filter(
                scrapped_date__icontains=date,scrappedBy__icontains=scrappedBy)
    else:
        if scrappedBy == None:
             data=Web_company_jobs.objects.values('company_info_id').annotate(dcount=Count('company_info_id')).filter(scrapped_date__icontains=getdate)
        else:
            data = Web_company_jobs.objects.values('company_info_id').annotate(dcount=Count('company_info_id')).filter(
                scrapped_date__icontains=date, scrappedBy__icontains=scrappedBy)
    return data
def BugsDashBoardRender(request):
    cid=request.GET.get('cinfoid')
    return  render(request,"Bugs.html",{'cid':cid})
def GetCred(request):
    auth=request.GET.get('auth')
    if auth=='jeeVAN':
        list=[
        {'username':'jeevan','password':'jeevan@123'},
        {'username':'anusha','password':'AnushA@123'},
       
        ]
        return JsonResponse({'data':list})
    else:
        return JsonResponse({'data':"please provide authentication"})
def raiseBug(request):
    assignBY=request.POST.get('assignby')
    cinfoid=request.POST.get('infoid')
    assignTo=request.POST.get('assignTo')
    Bugdesc=request.POST.get('Bugdesc')
    bug_image=request.FILES.getlist('bug_image')
    # pathname=request.POST['uploadIntern']
    datadict={
    'Resolved':'False',
    'Assigned_date':datetime.datetime.now(),
    'Bug_description':Bugdesc,
    'Bug_assigned_by':assignBY,
    'Bug_assigned_to':assignTo,
    'company_info_id':cinfoid
    }
    datasave=Bugs(**datadict)
    datasave.save()
    bug=Bugs.objects.filter(company_info_id=cinfoid).latest()
    for excelsheets in bug_image:
        path=DRIVE+r'jeevan\django\git\Storedatafrom-Excelsheets\storelocations\static\images'+str(bug.Bug_id)+".png"
        fileread=open(path,'wb+')
        for chunk in excelsheets.chunks():
            fileread.write(chunk)
        fileread.close()
    jobsDel=Web_company_jobs.objects.filter(company_info_id=cinfoid)
    interDel=Web_internships_jobs.objects.filter(company_info_id=cinfoid)
    for obj in jobsDel:
        obj.delete()
    for obj in interDel:
        obj.delete()
    try:
        elastic_reserch=requests.get('http://10.80.0.98:8080/gradsiren-jobs/dumpallscrapingjobstoes')
        if elastic_reserch.status_code==200:
            return bugList(request)
        else:
            return HttpResponse("Failed Elastic Search Updation But Bug Is raised !"+elastic_reserch.status_code)
    except:
        return bugList(request)
def bugList(request):
    dic={}
    if request.POST.get('infoid') != None or request.POST.get('bugid') != None :
        return render(request, 'Showbugs.html', {'ip': ip})
    if request.method=="GET":
        return render(request,'Showbugs.html',{'ip':ip})
    if request.method=="POST":
        for x in request.POST:
            if request.POST.get(x).strip()!='' or request.POST.get(x)!='select' or request.POST.get(x)!=None :
                dic[x]=request.POST.get(x)
        # assignto=request.POST.get('Bug_assigned_to')
        # rasby=request.POST.get('Bug_assigned_by')
        # resolv=request.POST.get("Resolved")
        # bugrasdate=request.POST.get('Assigned_date')
    else:
        for x in request.GET:
            if request.GET.get(x)!='' or request.GET.get(x)!='select'or request.GET.get(x)!=None:
                dic[x]=request.GET.get(x)
        # assignto = request.GET.get('AssignedTo')
        # rasby = request.GET.get('rasiedBy')
        # resolv = request.GET.get("resolved")
        # bugrasdate = request.GET.get('rasieddate')
    date=None
    datalist=[]
    delkey=[]
    for key,value in dic.items():
        if value=='select':
            delkey.append(key)
    for x in delkey:
        del dic[x]
    if dic.get('Assigned_date')=='':
        del dic['Assigned_date']
    del dic['csrfmiddlewaretoken']
    if  dic:
        data=Bugs.objects.filter(**dic)
    else:
        data = Bugs.objects.filter(Resolved="False")
    for obj in list(data)[-1::-1]:
        cname = None
        cnamdate = company_infoCopy.objects.filter(company_info_id=obj.company_info_id)
        if len(cnamdate) != 0:
            cname = cnamdate[0].company_name
        datalist.append({'company_info_id': obj.company_info_id, 'company_name': cname, 'bug_id': obj.Bug_id,
                         'assigned_by': obj.Bug_assigned_by, 'assignTo': obj.Bug_assigned_to,
                         'assignedDate': obj.Assigned_date})
    if request.POST.get('infoid')==None:
        if request.POST.get('bugid')==None:
            return render(request,'Showbugs.html',{'data':datalist,'ip':ip})
        else:
            return render(request,'Showbugs.html',{'data':datalist,'ip':ip,'status':'succses'})
    else:
        return render(request,'Showbugs.html',{'data':datalist,'ip':ip,'status':'succses'})
def viewBUg(request):
    bugId=request.GET.get('bugid')
    data=Bugs.objects.filter(Bug_id=bugId)
    if len(data)!=0:
        if data[0].Resolved=="True":
            res=None
        if data[0].Resolved=="False":
            res="False"
        dic={'cid':data[0].company_info_id,'bugdesc':data[0].Bug_description,'assignBy':data[0].Bug_assigned_by,'assignTo':data[0].Bug_assigned_to,'Resolved':res,'bug_id':bugId}
        return render(request,'viewbug.html',dic)
def ResolveBug(request):
    bugId=int(request.POST.get('bugid'))
    data=Bugs.objects.filter(Bug_id=bugId)
    if len(data)!=0:
        data[0].Resolved="True"
        data[0].ResolvedDate=datetime.datetime.now()
        data[0].save()
    return bugList(request)
def BugNotification(request):
    id=int(request.GET.get('bugid'))
    date=Bugs.objects.latest()
    return JsonResponse({"data":{"bugid":date.Bug_id,"Bug_assigned_to":date.Bug_assigned_to,"Bug_assigned_by":date.Bug_assigned_by}})
def deleteindividualsheet(request):
    path=r'D:/jeevan/django/excelsheets/'
    folder=request.GET.get('folder')
    sheet=request.GET.get('sheet')
    path=path+"{f}/{s}".format(f=folder,s=sheet)
    try:
        os.remove(path)
    except:
        pass
    return JsonResponse({"status":"sucsses"})
def pushcompayInfo(request):
    if request.method=="GET":
        return  render(request,"storecompany.html",{"form":UploadFiles})
    else:
        dic={}
        for x in request.POST:
            if request.POST.get(x)!='' and request.POST.get(x)!=None and str(request.POST.get(x)).lower()!='null' :
                dic[x]=request.POST.get(x)
        del dic['csrfmiddlewaretoken']
        if dic.get('company_unique_id')!=None:
            if len(company_infoCopy.objects.filter(company_unique_id=dic.get('company_unique_id')))!=0:
                return HttpResponse("company_unique_id aready exsitis")
        dic['addcompanystatus']="jeevan"
        data=company_infoCopy(**dic)
        data.save()
    return render(request,"storecompany.html",{"data":"success"})
def automated_deletion(model_obj):
    link=model_obj.apply_link
    try:
        delete_request=requests.get(model_obj.apply_link,timeout=1000)
    except:
        delte_file=open(DRIVE+r"""\\jeevan\\django\\storelocations\\DeletedLinks\\"""+str(datetime.datetime.today().date())+"""connectionError.txt""",'a')
        delte_file.write(link+"  connectionError  "+str(datetime.datetime.now())+"\n")
        delte_file.close()
    else:
        if delete_request.status_code>=400 and delete_request.status_code<=499:
            model_obj.delete()
            delte_file=open(DRIVE+r"""\\jeevan\\django\\storelocations\\DeletedLinks\\"""+str(datetime.datetime.today().date())+"""deleteLink.txt""",'a')
            delte_file.write(link+"   error400   "+str(datetime.datetime.now())+"\n")
            delte_file.close()
        elif delete_request.status_code>=200 and delete_request.status_code<=399:
            soup=BeautifulSoup(delete_request.text,"html.parser")
            for tag in soup.findAll('script'):
                tag.decompose()
            page_text=str(soup.get_text()).lower()
            error_list=['404 page not found','job is no longer available','page not found',' 404 ','the job you are looking for cannot be found','trying to apply for has been filled','Job Not Found','this job post no longer exists','job you have requested cannot be found','job post no longer exists',"you're looking for does not exist.",'job you are looking for cannot be found','your creativity and your career at HP. We’ve been waiting for you']
            for error in error_list:
                if error.lower() in page_text:
                    model_obj.delete()
                    delte_file=open(DRIVE+r"""\\jeevan\\django\\storelocations\\DeletedLinks\\"""+str(datetime.datetime.today().date())+"""deleteLink.txt""",'a')
                    delte_file.write(link+"  "+str(error)+"  "+str(datetime.datetime.now())+"\n")
                    delte_file.close()
                    break
        else:
            delte_file=open(DRIVE+r"""\\jeevan\\django\\storelocations\\DeletedLinks\\"""+str(datetime.datetime.today().date())+"""connectionError.txt""",'a')
            delte_file.write(link+" error500  "+str(datetime.datetime.now())+"\n")
            delte_file.close()

def thread_call(request):
    jobList=list(Web_company_jobs.objects.all())
    internLIST=list(Web_internships_jobs.objects.all())
    print("Deleting Jobs Started..........")
    x=0
    i=0
    while True:
        if len(jobList)==0:
            break
        try:
            automated_jobs_thread=threading.Thread(target=automated_deletion,name="automated_thread {}".format(x),args=[jobList.pop()])
            automated_jobs_thread.start()
            if len(internLIST)!=0:
                automated_interns_thread=threading.Thread(target=automated_deletion,name="automated_thread {}".format(x),args=[internLIST.pop()])
                automated_interns_thread.start()
                i+=1
            x+=1
        except:
            continue
        if x%150==0:
            automated_jobs_thread.join()
        if len(internLIST)!=0:
            if i%20==0:
                automated_interns_thread.join()
    print("jobs "+str(len(jobList))+"interns "+str(len(internLIST)))
    return HttpResponse("success")
def change_tested_status(request):
    tested_status=request.GET.get('tested_status')
    info_id=request.GET.get('info_id')
    if tested_status!=None:
        job_data=Web_company_jobs.objects.filter(company_info_id=info_id).update(tested_status="True")
        inetrnsdata=Web_internships_jobs.objects.filter(company_info_id=info_id).update(tested_status="True")
    return JsonResponse({"status":"success"})
def location_checker(request):
    dataList=[]
    postal_code=request.GET.get('postal_code')
    locations_data=Locations.objects.filter(postal_code=postal_code)
    if len(locations_data)!=0:
        dataList.append({'city':locations_data[0].city,'state':locations_data[0].state,'id':locations_data[0].location_id})
    return JsonResponse({'data':dataList})
def detecter(request):
    responser=[]
    data=Web_company_jobs.objects.filter()[0:500]
    print("started...")
    for x in data:
        exp=x.experience
        exp_level=x.experience_level
        detect_exp=None
        detect_exp_level=None
        string=""
        for y in  ('job_description','job_roles_responsibilities','qualifications'):
                if x.__dict__[y]!=None:
                    string=string+x.__dict__[y]
        if exp!=None:
            if string!="":
                detect_exp=detect_experince(exp)
        if detect_exp==None:
            detect_exp=detect_experince(BeautifulSoup(string,'html.parser').getText())
            print(detect_exp)
        detect_exp_level=detect_experience_level(detect_exp,string)
        x.experience=detect_exp
        x.experience_level=detect_exp_level
        x.save()
        responser.append({x.web_company_jobs_id:[detect_exp,detect_exp_level]})

    return JsonResponse({'data':responser})

def checkscrped(request,*args, **kwargs):
    data=request.GET.get('scrappedby')
    data1=request.GET.get('tested_status')
    if data!=None:
        return JsonResponse({data:list(Web_company_jobs.objects.values('scrappedBy','company_name').annotate(dcount=Count('scrappedBy')).filter(tested_status=data1,scrappedBy=data))})
    return JsonResponse({'status':"Failed...!",'error_':'please provid name'})

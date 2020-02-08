from django.shortcuts import render
from rest_framework.views import APIView
from StoreJobsRestservice.serializers import WebCompanyJobsSerilizer,WebInternshipJobsSerilizer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse,HttpResponse
from .models import WebCompanyJobs,WebInternshipJobs,TopCities,BeautifyCompanyJobs
import io
from django.shortcuts import render
import json
from rest_framework import status
from StoreJobsRestservice.instructions import Instructions,InstructionsForAll
from StoreJobsRestservice.removers import refining_job,HtmlParser,validatos,locationIdentifier
from fuzzywuzzy import fuzz
from StoreJobsRestservice.models import WebCompanyJobs,WebInternshipJobs
from copy import deepcopy
from .utils import Levenshtein,Soup
import time
import datetime
from dateutil import parser




# Create your views here.

class StoreJobsdata(APIView):
    @csrf_exempt
    def post(self,request):
        t1=time.time()
        try:
            scrapped_data_dict = JSONParser().parse(request)
        except Exception as exc:
            print(exc)
            return JsonResponse({'detail':'Please send json format'},status=status.HTTP_200_OK)
        response_list=list() 
        inserted_jobs_count=0
        inserted_internship_jobs_count=0
        duplicated_count=0
        exception_count=0 
        updated_jobs=0
        scrapped_count=len(scrapped_data_dict.get('data'))  
        for  scrapped_data in scrapped_data_dict.get('data'):
            try:
                data=refining_job(scrapped_data)
            except Exception as exc:
                print('1st',exc)
                exception_count+=1
                response_list.append({"status":"Failed...","desciption":str(exc)+" from refinig job",'job_title':scrapped_data.get('job_title')})
                continue
            try:
                if data.get('error')==None:
                    if data.get('type')=="INI":
                        obj=checking_duplicates(data.get('job'))
                        if obj==0:
                            serializer=WebInternshipJobsSerilizer(data=data.get('job'))
                            inserted_internship_jobs_count+=1
                            response_list.append({"status":"succses",'job_title':scrapped_data.get('job_title')})
                        elif obj==1:
                            response_list.append({"status":"Failed...","desciption":"duplicated internhip job",'job_title':scrapped_data.get('job_title')})
                            duplicated_count+=1
                            continue
                        else:
                            response_list.append({"status":"Succses","desciption":"posted date updated",'job_title':scrapped_data.get('job_title')})
                            updated_jobs+=1
                            continue

                    else:
                        obj=checking_duplicates(data.get('job'),'JOB')
                        if obj==0:
                            serializer=WebCompanyJobsSerilizer(data=data.get('job'))
                            inserted_jobs_count+=1
                            response_list.append({"status":"succses",'job_title':scrapped_data.get('job_title')})
                        elif obj==1:
                            response_list.append({"status":"Failed...","desciption":"duplicated  job",'job_title':scrapped_data.get('job_title')})
                            duplicated_count+=1
                            continue
                        else:
                            response_list.append({"status":"Succses","desciption":"posted date updated",'job_title':scrapped_data.get('job_title')})
                            updated_jobs+=1
                            continue 
                else:
                    print("3rd",str(data.get('error')))
                    exception_count+=1
                    response_list.append({"status":"Failed...","desciption":str(str(data.get('error')))+" refinig job give error",'job_title':scrapped_data.get('job_title')})
                    continue
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    exception_count+=1
                    response_list.append({"status":"Failed...","desciption":str(serializer.errors)+" serializer error",'job_title':scrapped_data.get('job_title')})
                    continue
            except Exception as exception:
                print("2nd",str(exception))
                exception_count+=1
                response_list.append({"status":"Failed...","desciption":str(exception)+" from storig  job",'job_title':scrapped_data.get('job_title')})
        t2=time.time()        
        t=t2-t1
        return JsonResponse({"status":"succses","response":response_list,"inserted_job_count":inserted_jobs_count,"interships_count":inserted_internship_jobs_count,"scrapped_count":scrapped_count,"exception_count":exception_count,"dupliacte_count":duplicated_count,"time_taken":t})        
def checking_duplicates(job,type='INI'):
    if type=="INI":
        if job.get('posted_date')==None:
            for obj in WebInternshipJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],deleted_status=None):
              if Levenshtein.get_similarty_percentage(Soup.text(obj.job_description),Soup.text(job.get('job_description')))>70:
                  return 1
            return 0      
        else:
            for obj in WebInternshipJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],apply_link=job['apply_link'],deleted_status=None):
                lev=Levenshtein.get_similarty_percentage(Soup.text(obj.job_description),Soup.text(job.get('job_description')))>70
                if lev>70:
                    if   parser.parse(job.get('posted_date').replace("00:00:00","00:05:00")).date()> parser.parse(str(obj.posted_date).replace("00:00:00","00:05:00")).date():
                        obj.posted_date=job.get('posted_date')
                        obj.scrapped_date=datetime.datetime.now()
                        obj.save()
                        return 3
                    return 1
            return 0  
    else:
        if job.get('posted_date')==None:
            for obj in WebCompanyJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],apply_link=job['apply_link'],deleted_status=None):
                if Levenshtein.get_similarty_percentage(Soup.text(obj.job_description),Soup.text(job.get('job_description')))>70:
                    return 1
            return 0  
        else:
            for obj in WebCompanyJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],apply_link=job['apply_link'],deleted_status=None):
                lev=Levenshtein.get_similarty_percentage(Soup.text(obj.job_description),Soup.text(job.get('job_description')))
                if lev>70:
                    if   parser.parse(job.get('posted_date').replace("00:00:00","00:05:00")).date()> parser.parse(str(obj.posted_date).replace("00:00:00","00:05:00")).date():
                        obj.posted_date=job.get('posted_date')
                        obj.save()
                        obj.scrapped_date=datetime.datetime.now()
                        return 3
                    return 1
            return 0  
def showjob(request,*args,**kwrgs):
    job={}
    if request.method=='GET':
        return render(request,'checkjob.html')
    for k,v in request.POST.items():
        if k!='csrfmiddlewaretoken':
            if  v.strip()!='':
                job[k]=v
    beautyfyObject=[]
    if job.get('company_info_id')!=None and job.get('company_info_id').strip()!='':
        beautyfyObject=BeautifyCompanyJobs.objects.filter(company_info_id=job.get('company_info_id'))
    if len(beautyfyObject)!=0:
        for obj in beautyfyObject:
            if obj.attrs==None and obj.keywords==None and obj.html_tags==None and obj.ul_li_tags==None:
                job =Instructions(obj.instruction_id,job).method_caller()
            else:
                query={}
                for column_name in ('html_tags','attrs','keywords','ul_li_tags'):
                    if (column_name=='attrs' or column_name=='ul_li_tags') and obj.__dict__.get(column_name)!=None:
                        query[column_name]=json.loads(obj.__dict__.get(column_name))
                        continue
                    if obj.__dict__.get(column_name)!=None:
                        query[column_name]=obj.__dict__.get(column_name)
                incobj=InstructionsForAll(job)
                job=incobj.rule_for_all(**query)
    optimizer={'job_description':HtmlParser,'posted_date':validatos,'job_location':locationIdentifier}
    for k,v in job.items():
        if k!='job_title' and k!='company_info_id':
            job[k]=optimizer.get(k)(v)
    data="<html>"
    for k,v in job.items():
        if k=='job_description':
            data=data+"<h5>{k}</h5><div class='job_description'>{v}</div>".format(k=k,v=v)
        else:    
            data=data+"<h5>{k}</h5><p>{v}</p>".format(k=k,v=v)
    data=data+"</html>"
    return HttpResponse(data)
def change_jobs(request):
    data_list=WebCompanyJobs.objects.filter(job_title__icontains="intern")
    count=0
    print(len(data_list))
    for job in data_list:
        typer=None
        serializer=None
        for value in (job.job_title,job.job_type,job.functional_area):
            value=str(value).strip().replace('-',' ')
            value=value.replace(',',' ').replace('/',' ').replace(":",' ').replace(';',' ').replace('(',' ').replace(')',' ')
            for identifiers in ('intern','intern.','intern,','intern ','internships-','internships','internships.','internships,','internships ','internship-','internship','internship.','internship,','internship ','fellowship','fellowship.','fellowship,','fellowship ','fellowships','fellowships.','fellowships,','fellowships ','aperentship','aperentship.','aperentship,','aperentship ','trainee','trainee.','trainee,','trainee ','apprenticeship','apprenticeship.','apprenticeship,','apprenticeship ','aperentships','aperentships.','aperentships,','aperentships '):
                if identifiers in [str(x).lower().strip() for x in value.split()] :
                    typer=True    
        if typer:
            print(job.job_title)
            job.delete()
            count+=1
    return HttpResponse(str(count))
       
     

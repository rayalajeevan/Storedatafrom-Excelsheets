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
from StoreJobsRestservice.models import WebCompanyJobs,WebInternshipJobs

# Create your views here.
class StoreJobsdata(APIView):
    @csrf_exempt
    def post(self,request):
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
                        if checking_duplicates(scrapped_data,data.get('job'))!=1:
                            serializer=WebInternshipJobsSerilizer(data=data.get('job'))
                            inserted_jobs_count+=1
                            response_list.append({"status":"succses",'job_title':scrapped_data.get('job_title')})
                        else:
                            response_list.append({"status":"Failed...","desciption":"duplicated internhip job",'job_title':scrapped_data.get('job_title')})
                            duplicated_count+=1
                            continue
                    else:
                        if checking_duplicates(scrapped_data,data.get('job'),'JOB')!=1:
                            serializer=WebCompanyJobsSerilizer(data=data.get('job'))
                            inserted_internship_jobs_count+=1
                            response_list.append({"status":"succses",'job_title':scrapped_data.get('job_title')})
                        else:
                            response_list.append({"status":"Failed...","desciption":"duplicated  job",'job_title':scrapped_data.get('job_title')})
                            duplicated_count+=1
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
            except Exception as exception:
                print("2nd",str(exception))
                exception_count+=1
                response_list.append({"status":"Failed...","desciption":str(exception)+" from storig  job",'job_title':scrapped_data.get('job_title')})
        return JsonResponse({"status":"succses","response":response_list,"inserted_job_count":inserted_jobs_count,"interships_count":inserted_internship_jobs_count,"scrapped_count":scrapped_count,"exception_count":exception_count,"dupliacte_count":duplicated_count})        
def checking_duplicates(scrapped_data,job,type='INI'):
    if type=="INI":
        if scrapped_data.get('posted_date')==None:
            if len(WebInternshipJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'),apply_link=job['apply_link']))==0:
                return 0
            else:
                return 1
        else:
            if len(WebInternshipJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'),apply_link=job['apply_link'],posted_date=job['posted_date']))==0:
                return 0
            else:
                return 1
    else:
        if scrapped_data.get('posted_date')==None:
            if len(WebCompanyJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'),apply_link=job['apply_link']))==0:
                return 0
            else:
                return 1
        else:
            if len(WebCompanyJobs.objects.filter(company_info_id=job['company_info_id'],job_title=job['job_title'],job_location=job['job_location'],job_id=job.get('job_id'),apply_link=job['apply_link'],posted_date=job['posted_date']))==0:
                return 0
            else:
                return 1
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
            if obj.attrs==None and obj.keywords==None and obj.html_tags==None:
                job =Instructions(obj.instruction_id,job).method_caller()
            else:
                query={}
                for column_name in ('html_tags','attrs','keywords'):
                    if column_name=='attrs' and obj.__dict__.get(column_name)!=None:
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

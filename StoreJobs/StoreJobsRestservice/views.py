from django.shortcuts import render
from rest_framework.views import APIView
from StoreJobsRestservice.serializers import WebCompanyJobsSerilizer,WebInternshipJobsSerilizer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse,HttpResponse
from .models import WebCompanyJobs,WebInternshipJobs,TopCities
import io
from django.shortcuts import render
from rest_framework import status
from StoreJobsRestservice.removers import refining_job,HtmlParser,validatos,locationIdentifier
from StoreJobsRestservice.models import WebCompanyJobs,WebInternshipJobs

# Create your views here.
class StoreJobsdata(APIView):
    # def get(self,request):
    #     path=r"C:\Users\Emphyd12146rjee1\Downloads\TopCity.xlsx"
    #     import pandas as pd
    #     titles=pd.read_excel(path)
    #     titles=dict(dict(titles)['City'])
    #     print("started.....")
    #     s=0
    #     d=0
    #     for x in titles.values():
    #         if len(x)>2:
    #             city=x.strip().split(',')[0]
    #             state=x.strip().split(',')[1]
    #             if len(TopCities.objects.filter(city_name=city.strip(),state_code=state.strip()))==0:
    #                 sav=TopCities(city_name=city.strip(),state_code=state.strip(),country_type="US",top_cities_type='default')
    #                 sav.save()
    #                 s+=1
    #             else:
    #                 d+=1
    #
    #     return JsonResponse({'s':s,'d':d})
    @csrf_exempt
    def post(self,request):
        try:
            scrapped_data = JSONParser().parse(request)
        except:
            return JsonResponse({'detail':'Please send json format'},status=status.HTTP_200_OK)
        try:
            data=refining_job(scrapped_data)
        except Exception as exc:
            print('1st',exc)
            return   JsonResponse({'detail':str(exc)},status=status.HTTP_200_OK)
        try:
            if data.get('error')==None:
                if data.get('type')=="INI":
                    if checking_duplicates(scrapped_data,data.get('job'))!=1:
                        serializer=WebInternshipJobsSerilizer(data=data.get('job'))
                    else:
                        return JsonResponse({'duplicateEntry':'Duplicated Job Cannot be enter'},status=status.HTTP_200_OK)
                else:
                    if checking_duplicates(scrapped_data,data.get('job'),'JOB')!=1:
                        serializer=WebCompanyJobsSerilizer(data=data.get('job'))
                    else:
                        return JsonResponse({'duplicateEntry':'Duplicated Job Cannot be enter'},status=status.HTTP_200_OK)
            else:
                return JsonResponse(data,status=status.HTTP_200_OK)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status':'succses'},status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(serializer.errors,status=status.HTTP_205_RESET_CONTENT)
        except Exception as exception:
            print('2nd',str(exception))
            return JsonResponse({'detail':str(exception)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
    optimizer={'job_description':HtmlParser,'posted_date':validatos,'job_location':locationIdentifier}
    for k,v in job.items():
        if k!='job_title':
            job[k]=optimizer.get(k)(v)
    data="<html>"
    for k,v in job.items():
        data=data+"<h5>{k}</h5><p>{v}</p>".format(k=k,v=v)
    data=data+"</html>"
    return HttpResponse(data)

from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from companyapp.models import CompanyInfo,Industries,Locations,Industries,CompanyIndustries
from rest_framework import status
import socket
from companyapp.serializers import CompanyInfoSerializers,IndustriesSerializers
from rest_framework.parsers import JSONParser
class PushUpdateCompany(APIView):
    def get_object(self,pk,*args,**kwrgs):
        try:
            obj=CompanyInfo.objects.get(company_info_id=pk)
            return obj
        except CompanyInfo.DoesNotExist:
            return 0
    def get_industry_object(self,string,*args,**kwrgs):
        try:
            obj=Industries.objects.get(industry=string)
            return obj
        except CompanyInfo.DoesNotExist:
            return 0

    def get_location_object(self,pk,*args,**kwrgs):
        try:
            obj=Locations.objects.get(location_id=pk)
            return obj
        except Locations.DoesNotExist:
            return 0
    def get(self,request,*args,**kwrgs):
        if request.GET.get('id')==None:
            return render(request,'CompanyHome.html',{'ip':str(socket.gethostbyname(socket.gethostname()))})
        else:
            object=self.get_object(request.GET.get('id'))
            if object==0:
                return Response({'status':'Id DoesNotExist'},status=status.HTTP_400_BAD_REQUEST)
            else:
                serialized_obj=CompanyInfoSerializers(object)
                return Response(serialized_obj.data,status=status.HTTP_200_OK)

    def put(self,request,*args,**kwrgs):
        industry=None
        try:
            validated_data=JSONParser().parse(request)
        except Exception as e:
            print(e)
            return Response({'status':'Incorrect data'},status=status.HTTP_400_BAD_REQUEST)
        object=self.get_object(validated_data.get('company_info_id'))
        if object==0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if validated_data.get('hq_locations_location')!=None and  validated_data.get('hq_locations_location').strip()!='':
            location_object=self.get_location_object(validated_data.get('hq_locations_location'))
            if location_object!=0:
                validated_data['hq_locations_location']=location_object
        serlizerobj=CompanyInfoSerializers(object)
        update=serlizerobj.update(object,validated_data)
        if validated_data.get('industry')!=None and  validated_data.get('industry').strip()!='':
            industry=[x.strip() for x in validated_data.get('industry').split(',')]
            for x in industry:
                if x!='':
                    industry_obj=self.get_industry_object(x)
                    companyIndustriesObj=CompanyIndustries(industry=industry_obj,company_info=object,industry_type='default')
                    companyIndustriesObj.save()
        return Response({'status':'succses'},status=status.HTTP_202_ACCEPTED)
    def post(self,request,*args,**kwrgs):
        try:
            validated_data=JSONParser().parse(request)
        except Exception as e:
            print(e)
            return Response({'status':'Incorrect data'},status=status.HTTP_400_BAD_REQUEST)

class GetIndustry(generics.ListAPIView):
    serializer_class=IndustriesSerializers
    def get_queryset(self):
        query = None
        data = self.request.GET
        query=data.get('industry__icontains')
        if query!=None:
            return Industries.objects.filter(industry__icontains=query)[0:6]
        else:
            return []
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

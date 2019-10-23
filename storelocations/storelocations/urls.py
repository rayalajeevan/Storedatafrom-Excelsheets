"""storelocations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from locationModifier.views import GetCompanyName,gethtml,getCompanyData,renderHtml,Fileuploader,deleteExcelSheets,viewfiles,ViewJobsCount,BugsDashBoardRender,raiseBug
from locationModifier import views
from companyapp.views import PushUpdateCompany,GetIndustry
urlpatterns = [
    path('admin/', admin.site.urls),
    path('getCompanyInfoID',GetCompanyName.as_view()),
    path('Home/',gethtml),
    path('comapnydata/',getCompanyData),
    path('jobView/',renderHtml),
    path('fileupload/',Fileuploader),
    path('deleteExcelSheets/',deleteExcelSheets,name='delete'),
    path('viewfiles/',viewfiles),
    path('viewdashboard/',views.ViewJobsCount),
    path('viewjobscount/',views.ViewJobsCOuntBYFilter.as_view()),
    path('viewinternscount/',views.ViewInternsCOuntBYFilter.as_view()),
    path('BugsDashBoard/',BugsDashBoardRender),
    path('RaiseBug/',raiseBug),
    path('showbugs/',views.bugList),
    path('viewbug',views.viewBUg),
    path('ResolveBug/',views.ResolveBug),
    path('getcred',views.GetCred),
    # path('bugnotification/',views.BugNotification),
    path('deleteindividualsheet/',views.deleteindividualsheet),
    path('pushcompany/',PushUpdateCompany.as_view()),
    # path('deleteautomate/',views.thread_call),
    path('change_tested_status/',views.change_tested_status),
    path('getlocationid/',views.location_checker),
    path('getIndustries/',GetIndustry.as_view()),
    path('keywordjobs/',views.detecter),
    path('checktested/',views.checkscrped)
]

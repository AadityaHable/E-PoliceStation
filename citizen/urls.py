"""epolicestation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from citizen import views
# from myapp import views  
# from django.conf.urls import url

urlpatterns = [  
    # path('admin/', admin.site.urls),  
    # #path('',views.index),
    # url(r'^export-exl/$', views.export, name='export'),
    path('export-json/', views.export, name='export'),
     #url(r'^export-csv/$', views.export, name='export'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register_page/', views.register_page, name='register_page'),
    path('register_member/', views.register_member, name='register_member'),
    path('login_evaluate/', views.login_evaluate, name='login_evaluate'),
    path('logout/', views.logout, name='logout'),
    path('law_details/',views.law_details, name='law_details'),
    path('citizen_dashboard/',views.citizen_dashboard,name='citizen_dashboard'),
    path('main_fir/',views.main_fir,name="main_fir"),
    path('add_fir/<int:pk>', views.add_fir, name='add_fir'),
    path('view_fir/',views.view_fir, name="view_fir"),
    path('view_details/<int:pk>',views.view_details, name="view_details"),
    path('ins_view_details/<int:pk>',views.ins_view_details, name="ins_view_details"),
    path('com_view_details/<int:pk>',views.com_view_details, name="com_view_details"),
    path('submit_fir/', views.submit_fir, name='submit_fir'),
    path('add_complaint/',views.add_complaint, name='add_complaint'),
    path('add_feedback/',views.add_feedback, name='add_feedback'),
    path('view_feedback/',views.view_feedback, name='view_feedback'),
    path('submit_feedback/',views.submit_feedback,name='submit_feedback'),
    path('submit_complaint/',views.submit_complaint, name='submit_complaint'),
    path('verify_otp/',views.verify_otp, name='verify_otp'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('enter_new_password/',views.enter_new_password,name='enter_new_password'),
    path('login_change_password/',views.login_change_password,name='login_change_password'),
    path('view_complaint_citizen/',views.view_complaint_citizen,name='view_complaint_citizen'),
    path('get_sub/',views.get_sub,name='get_sub'),
    path('inspector_dashboard/',views.inspector_dashboard,name="inspector_dashboard"),
    path('inspector_view_complaint/',views.inspector_view_complaint,name="inspector_view_complaint"),
    path('inspector_view_fir/',views.inspector_view_fir,name="inspector_view_fir"),
    path('inspector_add_feedback/',views.inspector_add_feedback,name="inspector_add_feedback"),
    path('inspector_view_feedback/',views.inspector_view_feedback,name="inspector_view_feedback"),
    path('ajax/load_category',views.load_category,name='ajax_load_category'),
    path('commissioner_dashboard/',views.commissioner_dashboard,name="commissioner_dashboard"),
    path('commissioner_view_complaint/',views.commissioner_view_complaint,name="commissioner_view_complaint"),
    path('commissioner_add_feedback/',views.commissioner_add_feedback,name="commissioner_add_feedback"),
    path('commissioner_view_feedback/',views.commissioner_view_feedback,name="commissioner_view_feedback"),
    path('delete_complaint/<int:pk>',views.delete_complaint,name="delete_complaint"),
    path('view_fir_commissioner/',views.view_fir_commissioner,name="view_fir_commissioner"),
    path('search-fir/',views.search_fir,name="search-fir"),
    path('delete_fir/<int:pk>',views.delete_fir,name="delete_fir"),
    path('close_fir/<int:pk>',views.close_fir,name="close_fir"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('update_profile_page/',views.update_profile_page,name="update_profile_page"),
    path('ins_update_profile/',views.ins_update_profile,name="ins_update_profile"),
    path('ins_update_profile_page/',views.ins_update_profile_page,name="ins_update_profile_page"),
    path('com_update_profile/',views.com_update_profile,name="com_update_profile"),
    path('com_update_profile_page/',views.com_update_profile_page,name="com_update_profile_page"),
    path('view_fir_report/',views.view_fir_report,name="view_fir_report"),
    # path('fir_report_pdf/',views.fir_report_pdf,name="fir_report_pdf"),
    path('reportview/',views.reportview,name="reportview"),
    path('generate_report/',views.generate_report,name="generate_report"),
    path('view_complaint_report/',views.view_complaint_report,name="view_complaint_report"),
    path('generate_complaint_report/',views.generate_complaint_report,name="generate_complaint_report"),

    


   
]

   

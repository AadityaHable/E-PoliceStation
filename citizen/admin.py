from django.contrib import admin
from .models import *
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# from myapp.models import User



admin.site.site_url='http://127.0.0.1:8000/'

# @dmin.register(User)
# class UserAdmin(ImportExportModelAdmin):
#     list_display = ("email","is_active","role","is_verfied")
#     pass

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    #exclude = ('created_date', 'updated_date')
    list_display= ('email','is_active','role','is_verfied')
    list_display_links= ('email',)
    list_editable= ('is_active','is_verfied',) 
    list_per_page = 15
    search_fields= ('email',)
    list_filter = ('created_at','role')
    

@admin.register(citizen)
class citizenAdmin(ImportExportModelAdmin):
    #exclude = ('created_date', 'updated_date')
    list_display= ('firstname','lastname','profile_pic','contact_no','address','gender','dob')
    list_display_links= ('firstname',)
    search_fields= ('firstname',)
    list_filter = ('gender','firstname',)    

    def export_audits_as_pdf(self, request, queryset):
        file_name = "audit_entries{0}.pdf".format(time.strftime("%d-%m-%Y-%H-%M-%S"))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)

        data = [['firstname', 'lastname', 'contact_no']]
        for d in queryset.all():
            datetime_str = str(d.action_time).split('.')[0]
            item = [datetime_str, d.firstname, d.lastname, d.contact_no]
            data.append(item)

        doc = SimpleDocTemplate(response, pagesize=(21*inch, 29*inch))
        elements = []

        table_data = Table(data)
        table_data.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                        ("FONTSIZE",  (0, 0), (-1, -1), 13)]))
        elements.append(table_data)
        doc.build(elements)

        return response

@admin.register(commissioner)
class commissionerAdmin(ImportExportModelAdmin):
    #exclude = ('created_date', 'updated_date')
    list_display= ('firstname','lastname','profile_pic','contact_no','city')
    list_display_links= ('firstname',)
    list_editable= ('profile_pic','contact_no',)
    list_per_page = 2

@admin.register(inspector)
class inspectorAdmin(ImportExportModelAdmin):
    #exclude = ('created_date', 'updated_date')
    list_display= ('firstname','lastname','profile_pic','contact_no','dob','address','gender','contact_no')
    list_display_links= ('firstname',)
    search_fields= ('firstname',)
    list_filter = ('area','firstname')

@admin.register(complaint)
class complaintAdmin(ImportExportModelAdmin):
    #exclude = ('created_date', 'updated_date')
    search_fields= ('firstname',)
    list_filter = ('complaint_date','pname')  

@admin.register(feedback)
class feedbackAdmin(ImportExportModelAdmin):
    list_display= ('ratings','user_id','citizen_id','feedback_desc','feedback_date')
    list_display_links= ('user_id',)
    search_fields= ('ratings',)
    list_filter = ('ratings','feedback_date')

@admin.register(policestation)
class policestationAdmin(ImportExportModelAdmin):
    list_display= ('policestation_name','inspector_id','policestation_city','policestation_area','policestation_address','policestation_contact_no')
    list_display_links= ('policestation_name',)
    search_fields= ('policestation_name',)
    list_filter = ('policestation_area','policestation_city')

@admin.register(crime_category)
class crime_categoryAdmin(ImportExportModelAdmin):
    list_display= ('crime_category_name','cat_img')
    search_fields= ('crime_category_name',)

@admin.register(Sub_crime)
class Sub_crimeAdmin(ImportExportModelAdmin):
    list_display= ('crime_id','sub_category_name')
    search_fields= ('sub_category_name',)
    list_filter = ['crime_id']

@admin.register(FIR)
class FIRAdmin(ImportExportModelAdmin):
    search_fields= ('firstname',)
    list_filter = ('gender','FIR_date','policestation_id','crime_id','subcrime_id')  
  
    


#admin.site.register(User,UserAdmin)
#admin.site.register(citizen,citizenAdmin)
# admin.site.register(law)
# admin.site.register(crime_category,crime_categoryAdmin)
# admin.site.register(Sub_crime,Sub_crimeAdmin)
# admin.site.register(complaint,complaintAdmin)
# # admin.site.register(commissioner,commissionerAdmin)
# admin.site.register(inspector,inspectorAdmin)
# admin.site.register(feedback,feedbackAdmin)
# admin.site.register(policestation,policestationAdmin)
# admin.site.register(FIR,FIRAdmin)
# Register your models here.

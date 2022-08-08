from django.shortcuts import render,HttpResponseRedirect,reverse,HttpResponse
from .models import *
from .utils import *
from random import randint
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
# from django.shortcuts import render, redirect
import re
# from django.http import HttpResponse
from .resources import UserResource

from django.db.models import Q

# Create your views here.
import tempfile
from reportlab.pdfgen import canvas
from django.template import Context
from xhtml2pdf import pisa
from io import StringIO

from django.template.loader import render_to_string,get_template

import datetime


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path


def export(request):
	user_resource= UserResource()
	dataset = user_resource.export()
	response = HttpResponse(dataset.csv, content_type='text/csv')
	response ['Content-Disposition'] = 'attachment; filename="user.csv"'
	response = HttpResponse(dataset.json, content_type='application/json')
	response['Content-Disposition'] = 'attachment; filename="persons.json"'
	response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename="persons.xls"'
	# response = HttpResponse(dataset.xls, content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="persons.pdf"'
	return response

def index(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])	
		cid=citizen.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'feedback_data':feedback_data,
				'data':data,
				'uid':uid,
				'cid':cid,
		}
		return render(request,"citizen/index.html",{'context':context})
	elif "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				
				'data':data,
				'uid':uid,
				'cmid':cmid,
				'feedback_data':feedback_data,
		}
		return render(request,"commissioner/index.html",{'context':context})
	elif "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				
				'data':data,
				'uid':uid,
				'ins_id':ins_id,
				'feedback_data':feedback_data,
		}
		return render(request,"inspector/index.html",{'context':context})
	else:
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'data':data,
				'feedback_data':feedback_data,
		}
		return render(request,"citizen/index.html",{'context':context})

def register_page(request):
	return render(request,"citizen/register.html")

def register_member(request):
	role="Citizen"
	email=request.POST['email']
	firstname= request.POST['fname']
	lastname= request.POST['lname']
	contact_no= request.POST['contact_no']

	password=email[:4]+str(randint(11,99))+contact_no[-3:]
	
	uid=User.objects.create(email=email,password=password,role=role)
	cid=citizen.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact_no=contact_no)
	sendmail("Authentication",'send_password',email,{'name':cid.firstname,'password':password})
	return render(request,"login.html")


def login(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'data':data,
				'uid':uid,
				'cid':cid,				
				'feedback_data':feedback_data,
		}
		return render(request,"citizen/index.html",{'context':context})
	elif "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'data':data,
				'uid':uid,
				'cmid':cmid,
				'feedback_data':feedback_data,				
		}
		return render(request,"commissioner/index.html",{'context':context})
	elif "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'data':data,
				'uid':uid,
				'ins_id':ins_id,
				'feedback_data':feedback_data,				
		}
		return render(request,"inspector/index.html",{'context':context})
	else:
		return render(request,"login.html")

def login_evaluate(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'uid':uid,
				'cid':cid,
				'data':data,
				'feedback_data':feedback_data,	
		}
		
		for i in feedback_data:
			print("------------>",i.feedback_desc)
		return render(request,"citizen/index.html",{'context':context})
	elif "cm_email" in request.session:  #For commissioner
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'uid':uid,
				'cmid':cmid,
				'data':data,
				'feedback_data':feedback_data,
		}
		for i in feedback_data:
			print("------------>",i.feedback_desc)
		return render(request,"commissioner/index.html",{'context':context})
	elif "ins_email" in request.session:  #For inspector
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		data=law.objects.all()
		feedback_data=feedback.objects.all()
		context={
				'uid':uid,
				'ins_id':ins_id,
				'data':data,
				'feedback_data':feedback_data,
		}
		for i in feedback_data:
			print("------------>",i.feedback_desc)
		return render(request,"inspector/index.html",{'context':context})
	else:	
		try:
			role=request.POST['role']
			try:
				u_email=request.POST['email']
				u_password=request.POST['password']
				u_role=request.POST['role']
				uid=User.objects.get(email=u_email)
				if uid.is_verfied==False:
					if uid.role=="Citizen":
						cid=citizen.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							#request.session['c_email']=u_email
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							context={
								
								'uid':uid,
								'cid':cid,
								'data':data,
								'feedback_data':feedback_data,
							}

							return render(request,"loginverification.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					
					elif uid.role=="Commissioner":
						cmid=commissioner.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							# request.session['cm_email']=uid.email
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							context={
									'uid':uid,
									'cmid':cmid,
									'data':data,
									'feedback_data':feedback_data,
							}
							return render(request,"loginverification.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					elif uid.role=="Inspector":
						ins_id=inspector.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							# request.session['ins_email']=u_email
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							context={
									'uid':uid,
									'ins_id':ins_id,
									'data':data,
									'feedback_data':feedback_data,
							}
							return render(request,"loginverification.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					else:
						e_msg="select role"
						return render(request,"login.html",{'e_msg':e_msg})
				else:
					if uid.role=="Citizen":
						cid=citizen.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							request.session['c_email']=uid.email
							context={
								'data':data,
								'uid':uid,
								'cid':cid,
								'feedback_data':feedback_data,
							}
							return render(request,"citizen/index.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					elif uid.role=="Commissioner":
						cmid=commissioner.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							request.session['cm_email']=uid.email
							context={
								'data':data,
								'uid':uid,
								'cmid':cmid,
								'feedback_data':feedback_data,
							}
							return render(request,"commissioner/index.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					elif uid.role=="Inspector":
						ins_id=inspector.objects.get(user_id=uid)
						if uid.password==u_password and uid.role==u_role:
							data=law.objects.all()
							feedback_data=feedback.objects.all()
							request.session['ins_email']=uid.email
							context={
								'data':data,
								'uid':uid,
								'ins_id':ins_id,
								'feedback_data':feedback_data,
							}
							return render(request,"inspector/index.html",{'context':context})
						else:
							e_msg="Incorrect Password or role"
							return render(request,"login.html",{'e_msg':e_msg})
					else:
						e_msg="select role"
						return render(request,"login.html",{'e_msg':e_msg})
			except Exception as e:
				print("--->",e)
				e_msg="Invalid email or password"
				return render(request,"login.html",{'e_msg':e_msg})
		except Exception as e:
			print("--->",e)
			e_msg="Select Role"
			return render(request,"login.html",{'e_msg':e_msg})

def logout(request):
	if "c_email" in request.session:
		del request.session['c_email']
		print("------------------> logout")
		return render(request,"login.html")
	
	elif "cm_email" in request.session:  #For commissioner
		del request.session['cm_email']
		print("---------------->logout")
		return render(request,"login.html")
	
	elif "ins_email" in request.session:  #For inspector
		del request.session['ins_email']
		print("---------------->logout")
		return render(request,"login.html")
	else:
		return render(request,"login.html")


def law_details(request):
	return render(request,"citizen/index.html")

def citizen_dashboard(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		c_count=citizen.objects.all().count()
		policeall=policestation.objects.all()
		p_count=policestation.objects.all().count()
		print("---->",policeall)
		context={
				'cid':cid,
				'uid':uid,
				'c_count':c_count,
				'policeall':policeall,
				'p_count':p_count,
		}				
		return render(request,"citizen/citizen_dashboard.html",{'context':context})
	# elif "cm_email" in request.session:
	# 	uid=User.objects.get(email=request.session['cm_email'])
	# 	cmid=commissioner.objects.get(user_id=uid)
	# 	c_count=citizen.objects.all().count()
	# 	policeall=policestation.objects.all()
	# 	p_count=policestation.objects.all().count()
	# 	print("---->",policeall)
	# 	context={
	# 			'cmid':cmid,
	# 			'uid':uid,
	# 			'c_count':c_count,
	# 			'policeall':policeall,
	# 			'p_count':p_count,
	# 	}				
	# 	return render(request,"citizen/citizen_dashboard.html",{'context':context})
	# elif "ins_email" in request.session:
	# 	uid=User.objects.get(email=request.session['ins_email'])
	# 	ins_id=inspector.objects.get(user_id=uid)
	# 	c_count=citizen.objects.all().count()
	# 	policeall=policestation.objects.all()
	# 	p_count=policestation.objects.all().count()
	# 	print("---->",policeall)
	# 	context={
	# 			'ins_id':ins_id,
	# 			'uid':uid,
	# 			'c_count':c_count,
	# 			'policeall':policeall,
	# 			'p_count':p_count,
	# 	}				
	# 	return render(request,"citizen/citizen_dashboard.html",{'context':context})

def inspector_dashboard(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		c_count=citizen.objects.all().count()
		policeall=policestation.objects.all()
		p_count=policestation.objects.all().count()
		print("---->",policeall)
		context={
				'ins_id':ins_id,
				'uid':uid,
				'c_count':c_count,
				'policeall':policeall,
				'p_count':p_count,
		}				
	return render(request,"inspector/inspector_dashboard.html",{'context':context})

def commissioner_dashboard(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		c_count=citizen.objects.all().count()
		policeall=policestation.objects.all()
		p_count=policestation.objects.all().count()
		print("---->",policeall)
		context={
				'cmid':cmid,
				'uid':uid,
				'c_count':c_count,
				'policeall':policeall,
				'p_count':p_count,
		}				
	return render(request,"commissioner/commissioner_dashboard.html",{'context':context})

def main_fir(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		police_stat=policestation.objects.all()
		cat=crime_category.objects.all()
		context={
				'cid':cid,
				'uid':uid,
				'police_stat':police_stat,
				'cat':cat,
		}
	return render(request,"citizen/main_fir.html",{'context':context})

def add_fir(request,pk):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		#crime_cat=crime_category.objects.all()
		police_stat=policestation.objects.all()
		subcrime_cat=Sub_crime.objects.filter(crime_id=pk)
		context={
				'cid':cid,
				'uid':uid,
				'police_stat':police_stat,
				'subcrime_cat':subcrime_cat,
				'pk':pk,
		}				
		return render(request,"citizen/add_fir.html",{'context':context})
def submit_fir(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		cid_value=str(cid.contact_no)
		fir_id_value=FIR.objects.last()
		if fir_id_value:
			F_id=fir_id_value.id
			FIR_no=cid_value[-3:]+str(cid.id)+str(F_id)
			print("---> FIR no if : ",FIR_no)
		else:	
			FIR_no=cid_value[-3:]+str(cid.id)
			print("---> FIR no else : ",FIR_no)
		
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		dob=request.POST['dateofbirth']
		gender=request.POST['gender']
		crimeid=request.POST['crimecat']
		crimeid_id=crime_category.objects.get(id=crimeid)  #

		print(gender)

		policestation_id=request.POST['policestation']
		policeid_id=policestation.objects.get(id=policestation_id)
		sub_category_id=request.POST['sub_category_name']
		sub_id=Sub_crime.objects.get(id=sub_category_id)  #

		# proof_img=request.POST['proof_img']
		# proof_video=request.POST['proof_video']
		email=request.POST['email']
		FIR_description=request.POST['FIR_description']
		contact_no=request.POST['contact_no']
		print("------------------->",FIR_no)

		if "proof_img" in request.FILES and "proof_video" in request.FILES:
			proof_img=request.FILES['proof_img']
			proof_video=request.FILES['proof_video']
			FIR_id=FIR.objects.create(citizen_id=cid,FIR_description=FIR_description,
			FIR_no=FIR_no,proof_img=proof_img,proof_video=proof_video,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_id=policeid_id,crime_id=crimeid_id,email=email,contact_no=contact_no,
			subcrime_id=sub_id)
			return HttpResponseRedirect(reverse('citizen_dashboard'))


		elif "proof_video" in request.FILES:
			proof_video=request.FILES['proof_video']
			FIR_id=FIR.objects.create(citizen_id=cid,FIR_description=FIR_description,
			FIR_no=FIR_no,proof_video=proof_video,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_id=policeid_id,crime_id=crimeid_id,email=email,contact_no=contact_no,
			subcrime_id=sub_id)
			return HttpResponseRedirect(reverse('citizen_dashboard'))


		elif "proof_img" in request.FILES:
			proof_img=request.FILES['proof_img']
			FIR_id=FIR.objects.create(citizen_id=cid,FIR_description=FIR_description,
			FIR_no=FIR_no,proof_img=proof_img,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_id=policeid_id,crime_id=crimeid_id,email=email,contact_no=contact_no,
			subcrime_id=sub_id)
			return HttpResponseRedirect(reverse('citizen_dashboard'))

			
		else:
			FIR_id=FIR.objects.create(citizen_id=cid,FIR_description=FIR_description,
			FIR_no=FIR_no,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_id=policeid_id,crime_id=crimeid_id,email=email,contact_no=contact_no,
			subcrime_id=sub_id)
			
			print("---->FIR",FIR_id)
			return HttpResponseRedirect(reverse('citizen_dashboard'))

def view_fir(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
	context={
			'cid':cid,
			'uid':uid,

	}				

	return render(request,"citizen/view_fir_citizen.html",{'context':context})	

def view_details(request,pk):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		fid=FIR.objects.get(id=pk)
	context={
			'cid':cid,
			'uid':uid,	
			'fid':fid,
	}
	print("-------------->fid",fid)
	return render(request,"citizen/view_details.html",{'context':context})	

def ins_view_details(request,pk):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		fid=FIR.objects.get(id=pk)
	context={
			'ins_id':ins_id,
			'uid':uid,	
			'fid':fid,
	}
	print("-------------->fid",fid)
	return render(request,"inspector/ins_view_details.html",{'context':context})

def com_view_details(request,pk):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		fid=FIR.objects.get(id=pk)
	context={
			'cmid':cmid,
			'uid':uid,	
			'fid':fid,
	}
	print("-------------->fid",fid)
	return render(request,"commissioner/com_view_details.html",{'context':context})


def search_fir(request):
	if "c_email" in request.session:
		fno=request.POST['fno']
		print("------------------> FIR NO ",fno)
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		fid=FIR.objects.filter(FIR_no=fno)
		print("------------->FID",fid)
	context={
			'cid':cid,
			'uid':uid,	
			'fid':fid,
	}				

	return render(request,"citizen/view_fir_citizen.html",{'context':context})	

def add_complaint(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		police_stat=policestation.objects.all()
	context={
			'cid':cid,
			'uid':uid,
			'police_stat':police_stat
	}				
	return render(request,"citizen/add_complaint.html",{'context':context})

def add_feedback(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
	context={
			'cid':cid,
			'uid':uid,
	}	
	return render(request,"citizen/add_feedback.html",{'context':context})

def inspector_add_feedback(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
	context={
			'ins_id':ins_id,
			'uid':uid,
	}	
	return render(request,"inspector/inspector_add_feedback.html",{'context':context})

def commissioner_add_feedback(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
	context={
			'cmid':cmid,
			'uid':uid,
	}	
	return render(request,"commissioner/commissioner_add_feedback.html",{'context':context})

def view_feedback(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		feedbackall=feedback.objects.filter(user_id=uid)
		context={
					'cid':cid,
					'uid':uid,
					'feedbackall':feedbackall
		}				
		return render(request,"citizen/view_feedback.html",{'context':context})

def inspector_view_feedback(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		feedbackall=feedback.objects.filter(user_id=uid)
		context={
					'ins_id':ins_id,
					'uid':uid,
					'feedbackall':feedbackall
		}
	return render(request,"inspector/inspector_view_feedback.html",{'context':context})

def commissioner_view_feedback(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		feedbackall=feedback.objects.filter(user_id=uid)
		context={
					'cmid':cmid,
					'uid':uid,
					'feedbackall':feedbackall
		}
	return render(request,"commissioner/commissioner_view_feedback.html",{'context':context})

def submit_complaint(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		complaint_title= request.POST['complaint_title']
		complaint_description= request.POST['complaint_description']
		cid_value=str(cid.contact_no)
		complaint_id_value=complaint.objects.last()
		if complaint_id_value:
			com_id=complaint_id_value.id
			complaint_no=cid_value[-3:]+str(cid.id)+str(com_id)
			print("---> Complaint no if : ",complaint_no)
		else:	
			complaint_no=cid_value[-3:]+str(cid.id)
		
			print("---> Complaint no else : ",complaint_no)
		
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		dob=request.POST['dateofbirth']
		gender=request.POST['gender']
		print(gender)
		policestation_name=request.POST['policestation']

		print("------------------->",complaint_no)

		if "proof_img" in request.FILES and "proof_video" in request.FILES:
			proof_img=request.FILES['proof_img']
			proof_video=request.FILES['proof_video']
			complaint_id=complaint.objects.create(citizen_id=cid,complaint_title=complaint_title,complaint_description=complaint_description,
			complaint_no=complaint_no,proof_img=proof_img,proof_video=proof_video,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_name=policestation_name)

		elif "proof_video" in request.FILES:
			proof_video=request.FILES['proof_video']
			complaint_id=complaint.objects.create(citizen_id=cid,complaint_title=complaint_title,complaint_description=complaint_description,
			complaint_no=complaint_no,proof_video=proof_video,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_name=policestation_name)

		elif "proof_img" in request.FILES:
			proof_img=request.FILES['proof_img']
			complaint_id=complaint.objects.create(citizen_id=cid,complaint_title=complaint_title,complaint_description=complaint_description,
			complaint_no=complaint_no,proof_img=proof_img,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_name=policestation_name)
			
		else:
			complaint_id=complaint.objects.create(citizen_id=cid,complaint_title=complaint_title,complaint_description=complaint_description,
			complaint_no=complaint_no,firstname=firstname,lastname=lastname,dob=dob,
			gender=gender,policestation_name=policestation_name)

	return HttpResponseRedirect(reverse('citizen_dashboard'))
	# 	c_count=citizen.objects.all().count()
	# 	policeall=policestation.objects.all()
	# 	p_count=policestation.objects.all().count()
	# 	print("---->",policeall)
	# 	context={
	# 			'cid':cid,
	# 			'uid':uid,
	# 			'c_count':c_count,
	# 			'policeall':policeall,
	# 			'p_count':p_count,
	# 	}

	# return render(request,"citizen/citizen_dashboard.html",{'context':context})
def submit_feedback(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)

		ratings=request.POST['starRate']

		print("------------------------> ratings :",ratings)
		feedback_details= request.POST['feedback_desc']
		feedback_id=feedback.objects.create(user_id=uid,ratings=ratings,feedback_desc=feedback_details)
		return HttpResponseRedirect(reverse('citizen_dashboard'))
	
	elif "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)

		ratings=request.POST['starRate']
		print("------------------------> ratings :",ratings)
		feedback_details= request.POST['feedback_desc']
		feedback_id=feedback.objects.create(user_id=uid,ratings=ratings,feedback_desc=feedback_details)
		return HttpResponseRedirect(reverse('inspector_dashboard'))
	
	elif "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)

		ratings=request.POST['starRate']
		print("------------------------> ratings :",ratings)
		feedback_details= request.POST['feedback_desc']
		feedback_id=feedback.objects.create(user_id=uid,ratings=ratings,feedback_desc=feedback_details)
		return HttpResponseRedirect(reverse('commissioner_dashboard'))

def forgot_password(request):
	if request.method=="POST":
		email=request.POST['email']	
		try:
			user=User.objects.get(email=email)
			if user.role=="Citizen":
				cid=citizen.objects.get(user_id=user)
				otp=randint(1111,9999)
				user.otp=otp
				user.save()
				sendmail("Forgot Password",'mail_template',email,{'name':cid.firstname,'otp':otp})
				return render(request,'citizen/verify_otp.html',{'email':email})
			elif user.role=='Commissioner':
				cmid=commissioner.objects.get(user_id=user)
				otp=randint(1111,9999)
				user.otp=otp
				user.save()
				sendmail("Forgot Password",'mail_template',email,{'name':cmid.firstname,'otp':otp})
				return render(request,'citizen/verify_otp.html',{'email':email})
			elif user.role=='Inspector':
				ins_id=inspector.objects.get(user_id=user)
				otp=randint(1111,9999)
				user.otp=otp
				user.save()
				sendmail("Forgot Password",'mail_template',email,{'name':ins_id.firstname,'otp':otp})
				return render(request,'citizen/verify_otp.html',{'email':email})
		except Exception as e:
			print("------------->",e)
			e_msg="Email does not exist"
			return render(request,'citizen/forgot_password.html',{'e_msg':e_msg})

	return render(request,"citizen/forgot_password.html")

def verify_otp(request):
	otp=request.POST['otp']
	email=request.POST['email']
	uid=User.objects.get(email=email)
	context={
			'uid':uid
		}
	if str(uid.otp)==otp:
		
		return render(request,"citizen/enter_new_password.html",{'email':email,'context':context})
	else:
		e_msg="invalid otp"
		return render(request,"citizen/verify_otp.html",{'e_msg':e_msg,'email':email,'context':context})
	

def enter_new_password(request):
	try:
		email=request.POST['email']
		newpassword=request.POST['newpassword']
		cnewpassword=request.POST['cnewpassword']
		uid=User.objects.get(email=email)
		if newpassword==cnewpassword:
			user=User.objects.get(email=email)
			user.password=newpassword
			user.save()
			s_msg="Success : New password successfully updated !!"
			return render(request,'login.html',{'s_msg':s_msg})
		else:
			e_msg="New Password & Confirm New Password Does Not Matched"
			context={
				'uid':uid
			}
			return render(request,'citizen/enter_new_password.html',{'e_msg':e_msg,'context':context})
	except:
		return render(request,"citizen/forgot_password.html")

def login_change_password(request):
	email=request.POST['email']
	newpassword=request.POST['password']
	cnewpassword=request.POST['cpassword']
	uid=User.objects.get(email=email)
	if newpassword==cnewpassword:
		uid=User.objects.get(email=email)
		uid.password=newpassword
		uid.is_verfied=True
		uid.save()
		if uid.role=="Citizen":
			cid=citizen.objects.get(user_id=uid)
			data=law.objects.all()
			feedback_data=feedback.objects.all()
			request.session['c_email']=uid.email
			context={
				'data':data,
				'uid':uid,
				'cid':cid,
				'feedback_data':feedback_data,
			}
			return render(request,"citizen/index.html",{'context':context})
		elif uid.role=="Commissioner":
			cmid=commissioner.objects.get(user_id=uid)
			data=law.objects.all()
			feedback_data=feedback.objects.all()
			request.session['cm_email']=uid.email
			context={
				'data':data,
				'uid':uid,
				'cmid':cmid,
				'feedback_data':feedback_data,
			}
			return render(request,"commissioner/index.html",{'context':context})
		elif uid.role=="Inspector":
			ins_id=inspector.objects.get(user_id=uid)
			data=law.objects.all()
			feedback_data=feedback.objects.all()
			request.session['ins_email']=uid.email
			context={
				'data':data,
				'uid':uid,
				'ins_id':ins_id,
				'feedback_data':feedback_data,
			}
			return render(request,"inspector/index.html",{'context':context})
	else:
		e_msg="New Password & Confirm New Password Does Not Matched"
		context={
			'uid':uid
		}
		return render(request,'loginverification.html',{'e_msg':e_msg,'context':context})
			


def get_sub(request):
    name=request.POST['selected']
    print("------------->selected value ",name)
    pid=crime_category.objects.get(id=name)
    branddetails=Sub_crime.objects.filter(crime_id=pid)
    data=list(branddetails.values())
    context={
        'data':data,
    }
    print("------------------------>context :",data)
    return JsonResponse({'context':context})

def view_complaint_citizen(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])
		cid=citizen.objects.get(user_id=uid)
		complaintall=complaint.objects.filter(citizen_id=cid)
		context={
					'cid':cid,
					'uid':uid,
					'complaintall':complaintall
		}				
		return render(request,"citizen/view_complaint_citizen.html",{'context':context})

def inspector_view_complaint(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		complaintall=complaint.objects.all()
		ins_id=inspector.objects.get(user_id=uid)
		context={
				'ins_id':ins_id,
				'uid':uid,
				'complaintall':complaintall
		}
	return render(request,"inspector/inspector_view_complaint.html",{'context':context})

def delete_complaint(request,pk):
	cno=complaint.objects.get(complaint_no=pk)
	cno.delete()
	
	uid=User.objects.get(email=request.session['ins_email'])
	complaintall=complaint.objects.all()
	ins_id=inspector.objects.get(user_id=uid)
	context={
			'ins_id':ins_id,
			'uid':uid,
			'complaintall':complaintall
	}
	return render(request,"inspector/inspector_view_complaint.html",{'context':context})


def inspector_view_fir(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])
		ins_id=inspector.objects.get(user_id=uid)
		fid=FIR.objects.all()
		context={
				'ins_id':ins_id,
				'uid':uid,
				'fid':fid,
		}
	return render(request,"inspector/inspector_view_fir.html",{'context':context})

def commissioner_view_complaint(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		complaintall=complaint.objects.all()
		context={
				'cmid':cmid,
				'uid':uid,
				'complaintall':complaintall
		}
	return render(request,"commissioner/view_complaint_commissioner.html",{'context':context})

def load_category(request):
	print("Load Category CAlled....................................")
	category=request.GET.get('category')
	print(category)
	transactionSubcategory=Sub_crime.objects.filter(crime_id=category)
	print(transactionSubcategory)
	return render(request,'sample.html',{'transactionSubcategory':transactionSubcategory})


def delete_fir(request,pk):
	fno=FIR.objects.get(id=pk)
	fno.delete()
	uid=User.objects.get(email=request.session['ins_email'])
	fid=FIR.objects.all()
	ins_id=inspector.objects.get(user_id=uid)
	context={
			'ins_id':ins_id,
			'uid':uid,
			'fid':fid
	}
	return render(request,"inspector/inspector_view_fir.html",{'context':context})

def close_fir(request,pk):
	fno=FIR.objects.get(id=pk)
	fno.status="CLOSE"
	fno.save()
	uid=User.objects.get(email=request.session['ins_email'])
	fid=FIR.objects.all()
	ins_id=inspector.objects.get(user_id=uid)
	context={
			'ins_id':ins_id,
			'uid':uid,
			'fid':fid
	}
	return render(request,"inspector/inspector_view_fir.html",{'context':context})
def view_fir_commissioner(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])
		cmid=commissioner.objects.get(user_id=uid)
		fid=FIR.objects.all()
		context={
				'cmid':cmid,
				'uid':uid,
				'fid':fid,
		}
	return render(request,"commissioner/view_fir_commissioner.html",{'context':context})

def update_profile_page(request):
	if "c_email" in request.session:
		
		uid=User.objects.get(email=request.session['c_email'])	
		cid=citizen.objects.get(user_id=uid)
		context={
				'uid':uid,
				'cid':cid,
		}
	return render(request,"citizen/update_profile.html",{'context':context})


def update_profile(request):
	if "c_email" in request.session:
		uid=User.objects.get(email=request.session['c_email'])	
		cid=citizen.objects.get(user_id=uid)
		context={
				'uid':uid,
				'cid':cid,
		}
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		dob=request.POST['dateofbirth']
		gender=request.POST['gender']
		contact_no= request.POST['contact_no']
		address=request.POST['address']
		if "update_profile" in request.FILES:
			profile_pic=request.FILES['update_profile']
			cid.profile_pic=profile_pic

		cid.firstname=firstname
		cid.lastname=lastname
		cid.gender=gender
		cid.dob=dob
		cid.contact_no=contact_no
		cid.address=address
		cid.save()

		# cid=citizen.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact_no=contact_no,gender=gender,
		# address=address,dob=dob,profile_pic=profile_pic)

	return render(request,"citizen/update_profile.html",{'context':context})

def ins_update_profile_page(request):
	if "ins_email" in request.session:
		
		uid=User.objects.get(email=request.session['ins_email'])	
		ins_id=inspector.objects.get(user_id=uid)
		context={
				'uid':uid,
				'ins_id':ins_id,
		}
	return render(request,"inspector/ins_update_profile.html",{'context':context})


def ins_update_profile(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])	
		ins_id=inspector.objects.get(user_id=uid)
		context={
				'uid':uid,
				'ins_id':ins_id,
		}
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		dob=request.POST['dateofbirth']
		gender=request.POST['gender']
		contact_no= request.POST['contact_no']
		address=request.POST['address']
		if "update_profile" in request.FILES:
			profile_pic=request.FILES['update_profile']
			ins_id.profile_pic=profile_pic

		ins_id.firstname=firstname
		ins_id.lastname=lastname
		ins_id.gender=gender
		ins_id.dob=dob
		ins_id.contact_no=contact_no
		ins_id.address=address
		ins_id.save()

		# cid=citizen.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact_no=contact_no,gender=gender,
		# address=address,dob=dob,profile_pic=profile_pic)

	return render(request,"inspector/ins_update_profile.html",{'context':context})

def com_update_profile_page(request):
	if "cm_email" in request.session:
		
		uid=User.objects.get(email=request.session['cm_email'])	
		cmid=commissioner.objects.get(user_id=uid)
		context={
				'uid':uid,
				'cmid':cmid,
		}
	return render(request,"commissioner/com_update_profile.html",{'context':context})


def com_update_profile(request):
	if "cm_email" in request.session:
		uid=User.objects.get(email=request.session['cm_email'])	
		cmid=commissioner.objects.get(user_id=uid)
		context={
				'uid':uid,
				'cmid':cmid,
		}
		firstname=request.POST['firstname']
		lastname=request.POST['lastname']
		dob=request.POST['dateofbirth']
		gender=request.POST['gender']
		contact_no= request.POST['contact_no']
		address=request.POST['address']
		if "update_profile" in request.FILES:
			profile_pic=request.FILES['update_profile']
			cmid.profile_pic=profile_pic

		cmid.firstname=firstname
		cmid.lastname=lastname
		cmid.gender=gender
		cmid.dob=dob
		cmid.contact_no=contact_no
		cmid.address=address
		cmid.save()

		# cid=citizen.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact_no=contact_no,gender=gender,
		# address=address,dob=dob,profile_pic=profile_pic)

	return render(request,"commissioner/com_update_profile.html",{'context':context})

def fir_report(request):
	# citizen=citizen.objects.get(email=request.session['c_email'])
    # if request.method=="POST":
	# 	filter_name=request.POST['filter_name']
	# 	search=request.POST['search']
	# 	if filter_name=="fname":
	# 		all_fir=FIR.objects.filter(citizen=citizen,fname=search)
	# 		return render(request,'fir_report.html',{'all_fir':all_fir})
	# 	elif filter_name=="citizen_id":
	# 	    all_fir=FIR.objects.filter(citizen=citizen,citizen_id=search)
	# 	    return render(request,'fir_report.html',{'all_fir':all_fir})
	# else:
	# 	all_fir=FIR.objects.filter(citizen=citizen)
    #     return render(request,'fir_report.html',{'all_fir':all_fir})
	pass

def reportview(request):
	pass

# def fir_report_pdf(request):
# 	tutor=Tutor.objects.get(email=request.session['email'])
#     if request.POST['action'] == "search":
    
#         tutor=Tutor.objects.get(email=request.session['email'])
#         if request.method=="POST":
#             filter_name=request.POST['filter_name']
#             search=request.POST['search']
#             request.session['searchname']=search
#             request.session['filtername']=filter_name

#             print("=================> search value store ",search)
#             if filter_name=="bname":
#                 all_batch=Add_batch.objects.filter(tutor=tutor,bname=search)
#                 return render(request,'batch_report.html',{'all_batch':all_batch})
#             elif filter_name=="bnum":
#                 all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
#                 return render(request,'batch_report.html',{'all_batch':all_batch})
#         else:

#             all_batch=Add_batch.objects.filter(tutor=tutor)
#             return render(request,'batch_report.html',{'all_batch':all_batch})

    
#     elif request.POST['action'] == 'export':
#         print("--------------->export button click")
#         tutor=Tutor.objects.get(email=request.session['email'])
#         if request.method=="POST":
            
            
#             if "searchname" in request.session:
#                 search=request.session['searchname']
#                 filter_name=request.session['filtername']
#                 print("=================> search value store ",search)

#                 if filter_name=="bname":
#                     all_batch=Add_batch.objects.filter(tutor=tutor,bname=search)
#                     context = {'all_batch':all_batch}
#                     print("------------>> value pdf ")
                    
#                     template_path = 'batch_report_pdf.html'
#                     all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
#                     context = {'all_batch':all_batch}
#                     # Create a Django response object, and specify content_type as pdf
#                     response = HttpResponse(content_type='application/pdf')
#                     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#                     # find the template and render it.
#                     template = get_template(template_path)
#                     html = template.render(context)
#                     print("-----?> creating report ")
                    
#                     del request.session['searchname']
#                     del request.session['filtername']
#                     # if not pdf.err:
#                     #   return HttpResponse(result.getvalue(),content_type='application/pdf')
#                     # else:
#                     #   return HttpResponse('Errors')
#                     pisa_status = pisa.CreatePDF(
#                     html, dest=response, link_callback=link_callback)
#                     # if error then show some funy view
#                     if pisa_status.err:
#                         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#                     return response


#                 elif filter_name=="bnum":
#                     all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
#                     context = {'all_batch':all_batch}
#                     print("------------->>>> export pdf number wise ")
#                     # return render(request,'batch_report.html',{'all_batch':all_batch})
                    
#                     template_path = 'batch_report_pdf.html'
#                     all_batch=Add_batch.objects.filter(tutor=tutor,bnum=search)
#                     context = {'all_batch':all_batch}
#                     # Create a Django response object, and specify content_type as pdf
#                     response = HttpResponse(content_type='application/pdf')
#                     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#                     # find the template and render it.
#                     template = get_template(template_path)
#                     html = template.render(context)
#                     print("-----?> creating report ")
                    
#                     del request.session['searchname']
#                     del request.session['filtername']
#                     # if not pdf.err:
#                     #   return HttpResponse(result.getvalue(),content_type='application/pdf')
#                     # else:
#                     #   return HttpResponse('Errors')
#                     pisa_status = pisa.CreatePDF(
#                     html, dest=response, link_callback=link_callback)
#                     # if error then show some funy view
#                     if pisa_status.err:
#                         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#                     return response
#             else:
#                 all_batch=Add_batch.objects.all()   
#                 template_path = 'batch_report_pdf.html'
#                 context = {'all_batch':all_batch}
#                 # Create a Django response object, and specify content_type as pdf
#                 response = HttpResponse(content_type='application/pdf')
#                 response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#                 # find the template and render it.
#                 template = get_template(template_path)
#                 html = template.render(context)
#                 # if not pdf.err:
#                 #   return HttpResponse(result.getvalue(),content_type='application/pdf')
#                 # else:
#                 #   return HttpResponse('Errors')
#                 pisa_status = pisa.CreatePDF(
#                 html, dest=response, link_callback=link_callback)
#                 # if error then show some funy view
#                 if pisa_status.err:
#                     return HttpResponse('We had some errors <pre>' + html + '</pre>')
#                 return response     
#         else:
#             all_batch=Add_batch.objects.filter(tutor=tutor)
#             context = {'all_batch':all_batch}
#             print("---->>> else part of export ")
#             return render(request,'batch_report.html',{'all_batch':all_batch})

#         print("------------>> outside the if .. else")
#         all_batch=Add_batch.objects.all()   
#         template_path = 'batch_report_pdf.html'
#         context = {'all_batch':all_batch}
#         # Create a Django response object, and specify content_type as pdf
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#         # find the template and render it.
#         template = get_template(template_path)
#         html = template.render(context)
#         # if not pdf.err:
#         #   return HttpResponse(result.getvalue(),content_type='application/pdf')
#         # else:
#         #   return HttpResponse('Errors')
#         pisa_status = pisa.CreatePDF(
#         html, dest=response, link_callback=link_callback)
#         # if error then show some funy view
#         if pisa_status.err:
#             return HttpResponse('We had some errors <pre>' + html + '</pre>')
#         return response
#     else:
#         all_batch=Add_batch.objects.filter(tutor=tutor)
#         context = {'all_batch':all_batch}
        
#         del request.session['searchname']
#         del request.session['filtername']
#         return render(request,'batch_report.html',{'all_batch':all_batch})

def view_fir_report(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])	
		ins_id=inspector.objects.get(user_id=uid)
		fid=FIR.objects.all()
		sub=Sub_crime.objects.all()
		pall=policestation.objects.all()
	

		context={
				'uid':uid,
				'ins_id':ins_id,
				'fid':fid,
				'sub':sub,
				'pall':pall,
		}
		print("------------->sub ",sub)
	return render(request,"inspector/view_fir_report.html",{'context':context})


# pip install --upgrade --force-reinstall reportlab
# pip install xhtml2pdf
def generate_report(request):
	if request.POST['subcrime']:
		if request.POST['policestation']:
			if request.POST['status']:
				status=request.POST['status']

				subid = Sub_crime.objects.get(sub_category_name=request.POST['subcrime'])
				policestation_id = policestation.objects.get(policestation_name=request.POST['policestation'])
				content = "View by : "+request.POST['subcrime']+" and "+request.POST['policestation']+" STATUS :"+status
				today_date = datetime.date.today()


				all_FIR=FIR.objects.filter(subcrime_id=subid,policestation_id=policestation_id,status=status)   
				template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
				context = {
					'all_FIR':all_FIR,
					'today_date':today_date,
					'content':content,
					}
				print("----------------> get all data of FIR ",all_FIR)
				# Create a Django response object, and specify content_type as pdf
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="report.pdf"'
				# find the template and render it.
				template = get_template(template_path)
				html = template.render(context)
				# if not pdf.err:
				#   return HttpResponse(result.getvalue(),content_type='application/pdf')
				# else:
				#   return HttpResponse('Errors')
				pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
				# if error then show some funy view
				if pisa_status.err:
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response
			# police and subscrime
				subid = Sub_crime.objects.get(sub_category_name=request.POST['subcrime'])
				policestation_id = policestation.objects.get(policestation_name=request.POST['policestation'])

				today_date = datetime.date.today()
				content = "View by : "+request.POST['subcrime']+" and "+request.POST['policestation']
				print("------- clicked on generate report ",request.POST['subcrime'])

				all_FIR=FIR.objects.filter(subcrime_id=subid,policestation_id=policestation_id)   
				template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
				context = {
					'all_FIR':all_FIR,
					'today_date':today_date,
					'content':content,
					}
				print("----------------> get all data of FIR ",all_FIR)
				# Create a Django response object, and specify content_type as pdf
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="report.pdf"'
				# find the template and render it.
				template = get_template(template_path)
				html = template.render(context)
				# if not pdf.err:
				#   return HttpResponse(result.getvalue(),content_type='application/pdf')
				# else:
				#   return HttpResponse('Errors')
				pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
				# if error then show some funy view
				if pisa_status.err:
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response


		if request.POST['status']:
			status=request.POST['status']

			subid = Sub_crime.objects.get(sub_category_name=request.POST['subcrime'])
				
			content = "View by : "+request.POST['subcrime']+" and "+" STATUS :"+status
			today_date = datetime.date.today()


			all_FIR=FIR.objects.filter(subcrime_id=subid,status=status)   
			template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
			
			context = {
				'all_FIR':all_FIR,
				'today_date':today_date,
				'content':content,
				}
			print("----------------> get all data of FIR ",all_FIR)
			# Create a Django response object, and specify content_type as pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			# find the template and render it.
			template = get_template(template_path)
			html = template.render(context)
			# if not pdf.err:
			#   return HttpResponse(result.getvalue(),content_type='application/pdf')
			# else:
			#   return HttpResponse('Errors')
			pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			# if error then show some funy view
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			return response


		else:
			today_date = datetime.date.today()
			content = "View by : "+request.POST['subcrime']
			print("------- clicked on generate report ",request.POST['subcrime'])
			
			subid = Sub_crime.objects.get(sub_category_name=request.POST['subcrime'])

			all_FIR=FIR.objects.filter(subcrime_id=subid)   
			template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
			context = {
				'all_FIR':all_FIR,
				'today_date':today_date,
				'content':content,
				}
			print("----------------> get all data of FIR ",all_FIR)
			# Create a Django response object, and specify content_type as pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			# find the template and render it.
			template = get_template(template_path)
			html = template.render(context)
			# if not pdf.err:
			#   return HttpResponse(result.getvalue(),content_type='application/pdf')
			# else:
			#   return HttpResponse('Errors')
			pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			# if error then show some funy view
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			return response
	
	if request.POST['policestation']:
		if request.POST['status']:
			status=request.POST['status']

			
			policestation_id = policestation.objects.get(policestation_name=request.POST['policestation'])
			content = "View by : "+request.POST['policestation']+" STATUS :"+status
			today_date = datetime.date.today()

			all_FIR=FIR.objects.filter(policestation_id=policestation_id,status=status)   
			template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
			context = {
				'all_FIR':all_FIR,
				'today_date':today_date,
				'content':content,
				}
			print("----------------> get all data of FIR ",all_FIR)
			# Create a Django response object, and specify content_type as pdf
			response = HttpResponse(content_type='application/pdf')
			response['Content-Disposition'] = 'attachment; filename="report.pdf"'
			# find the template and render it.
			template = get_template(template_path)
			html = template.render(context)
			# if not pdf.err:
			#   return HttpResponse(result.getvalue(),content_type='application/pdf')
			# else:
			#   return HttpResponse('Errors')
			pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			# if error then show some funy view
			if pisa_status.err:
				return HttpResponse('We had some errors <pre>' + html + '</pre>')
			return response

		# only for police station 
		today_date = datetime.date.today()
		content = "View by : "+request.POST['policestation']
		print("------- clicked on generate report ",request.POST['policestation'])
		
		policestation_id = policestation.objects.get(policestation_name=request.POST['policestation'])

		all_FIR=FIR.objects.filter(policestation_id=policestation_id)   
		template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
		context = {
			'all_FIR':all_FIR,
			'today_date':today_date,
			'content':content,
			}
		print("----------------> get all data of FIR ",all_FIR)
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)
		# if not pdf.err:
		#   return HttpResponse(result.getvalue(),content_type='application/pdf')
		# else:
		#   return HttpResponse('Errors')
		pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response




	if request.POST['status']:
		status=request.POST['status']

		
		content = "View by : STATUS :"+status
		today_date = datetime.date.today()


		all_FIR=FIR.objects.filter(status=status)   
		template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
		context = {
			'all_FIR':all_FIR,
			'today_date':today_date,
			'content':content,
			}
		print("----------------> get all data of FIR ",all_FIR)
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)
		# if not pdf.err:
		#   return HttpResponse(result.getvalue(),content_type='application/pdf')
		# else:
		#   return HttpResponse('Errors')
		pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response


	# ALL FIR REPORT  ------------------------------
	today_date = datetime.date.today()
	content = "View By All FIR"
	print("------- clicked on generate report ")
	all_FIR=FIR.objects.all()   
	template_path = 'inspector/FIR_REPORT_PDF_FILE.html'
	context = {
		'all_FIR':all_FIR,
		'today_date':today_date,
		'content':content,
		}
	print("----------------> get all data of FIR ",all_FIR)
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)
	# if not pdf.err:
	#   return HttpResponse(result.getvalue(),content_type='application/pdf')
	# else:
	#   return HttpResponse('Errors')
	pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response

def view_complaint_report(request):
	if "ins_email" in request.session:
		uid=User.objects.get(email=request.session['ins_email'])	
		ins_id=inspector.objects.get(user_id=uid)
		complaintall=complaint.objects.all()
		pall=policestation.objects.all()
	

		context={
				'uid':uid,
				'ins_id':ins_id,
				'complaintall':complaintall,
				'pall':pall,
		}
		
	return render(request,"inspector/view_complaint_report.html",{'context':context})

def generate_complaint_report(request):
	if request.POST['policestation']:
			if request.POST['display']:
				print("----------------> policestation and gender wise report ")
				gender = request.POST['display']
				pname = request.POST['policestation']
				words = re.split(r"[^A-Za-z']+", pname)
				print("-----------------> words",words)
				content = "View by : "+request.POST['display']+" and "+request.POST['policestation']
				today_date = datetime.date.today()
				all_complaint=complaint.objects.filter(pname=words[0],gender=gender)   
				template_path = 'inspector/COMPLAINT_REPORT_PDF_FILE.html'
				context = {
					'all_complaint':all_complaint,
					'today_date':today_date,
					'content':content,
					}
				print("----------------> get all data of Complaint ",all_complaint)
				# Create a Django response object, and specify content_type as pdf
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="report.pdf"'
				# find the template and render it.
				template = get_template(template_path)
				html = template.render(context)
				# if not pdf.err:
				#   return HttpResponse(result.getvalue(),content_type='application/pdf')
				# else:
				#   return HttpResponse('Errors')
				pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
				# if error then show some funy view
				if pisa_status.err:
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response
			# only policestation
			else:
				#policestation_id = policestation.objects.get(policestation_name=request.POST['policestation'])
				#print("-------------------> policestation ",policestation_id)
				today_date = datetime.date.today()
				content = "View by : "+request.POST['policestation']
				print("------- clicked on generate report ",request.POST['policestation'])
				
				pname = request.POST['policestation']
				words = re.split(r"[^A-Za-z']+", pname)
				print("-----------------> words",words)
				all_complaint = complaint.objects.filter(pname=words[0])
				

				#all_complaint=complaint.objects.filter(Q(pname__icontains=pname))   
				template_path = 'inspector/COMPLAINT_REPORT_PDF_FILE.html'
				context = {
					'all_complaint':all_complaint,
					'today_date':today_date,
					'content':content,
					}
				print("----------------> get all data of complaint ",all_complaint)
				# Create a Django response object, and specify content_type as pdf
				response = HttpResponse(content_type='application/pdf')
				response['Content-Disposition'] = 'attachment; filename="report.pdf"'
				# find the template and render it.
				template = get_template(template_path)
				html = template.render(context)
				# if not pdf.err:
				#   return HttpResponse(result.getvalue(),content_type='application/pdf')
				# else:
				#   return HttpResponse('Errors')
				pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
				# if error then show some funy view
				if pisa_status.err:
					return HttpResponse('We had some errors <pre>' + html + '</pre>')
				return response
# only gender REPORT  ------------------------------	
	if request.POST['display']:
		gender=request.POST['display']
	
		content = "View by : GENDER :"+gender
		today_date = datetime.date.today()


		all_complaint=complaint.objects.filter(gender=gender)   
		template_path = 'inspector/COMPLAINT_REPORT_PDF_FILE.html'
		context = {
			'all_complaint':all_complaint,
			'today_date':today_date,
			'content':content,
			}
		print("----------------> get all data of Complaint ",all_complaint)
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)
		# if not pdf.err:
		#   return HttpResponse(result.getvalue(),content_type='application/pdf')
		# else:
		#   return HttpResponse('Errors')
		pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response	
	else:
		# ALL complaint REPORT  ------------------------------
		today_date = datetime.date.today()
		content = "View By All Complaint"
		print("------- clicked on generate report ")
		all_complaint=complaint.objects.all()   
		template_path = 'inspector/COMPLAINT_REPORT_PDF_FILE.html'
		context = {
			'all_complaint':all_complaint,
			'today_date':today_date,
			'content':content,
			}
		print("----------------> get all data of Complaint ",all_complaint)
		# Create a Django response object, and specify content_type as pdf
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="report.pdf"'
		# find the template and render it.
		template = get_template(template_path)
		html = template.render(context)
		# if not pdf.err:
		#   return HttpResponse(result.getvalue(),content_type='application/pdf')
		# else:
		#   return HttpResponse('Errors')
		pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
		# if error then show some funy view
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>' + html + '</pre>')
		return response

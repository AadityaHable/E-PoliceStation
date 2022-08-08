from django.db import models
from django.db.models import Model 
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField

def validate_geeks_mail(value): 
    if "@gmail.com" in value or "@yahoo.com" in value or "@gmail.in" in value or "@yahoo.in" in value or "@icloud.com" in value:
        return value 
    else: 
        raise ValidationError("This field accepts mail id of google,yahoo,apple only")

def validation(name):
    for char in name:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def lastname_validation(lname):
    for char in lname:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def role_validation(role):
    for char in role:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def commissionerfvalidation(name):
    for char in name:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def commissionerlvalidation(name):
    for char in name:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def citizenfvalidation(name):
    for char in name:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

def citizenlvalidation(name):
    for char in name:
        if  not (("A" <= char and char <= "Z") or ("a" <= char and char <= "z") or (char == " ")):
            raise ValidationError("This field accepts only characters")
    return True

GENDER_CHOICES=(
    ('M','MALE'),
    ('F','FEMALE')
)

# Create your models here.
class User(models.Model):
    email = models.CharField( max_length = 200, validators=[validate_geeks_mail]) 
    password = models.CharField(max_length = 20)
    otp = models.IntegerField(default = 459)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    role = models.CharField(max_length = 20, validators=[role_validation])
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)

    # class Meta:
    #     db_table = "web_user"
    
    def __str__(self):
        return self.email

class citizen(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50, validators=[citizenfvalidation])
    lastname = models.CharField(max_length=50, validators=[citizenlvalidation])
    profile_pic=models.FileField(upload_to='images/',default='default-pic.png')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format of intergers only . Up to 10 digits allowed.")
    contact_no=models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    address = models.CharField(max_length= 500, blank= True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob = models.DateField(blank=True,null=True)
    
    def __str__(self):
        return self.firstname

class commissioner(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50, validators=[commissionerfvalidation])
    lastname = models.CharField(max_length=50, validators=[commissionerlvalidation])
    profile_pic=models.FileField(upload_to='images/',default='default-pic.png')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format of intergers only . Up to 10 digits allowed.")
    contact_no=models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    address = models.CharField(max_length= 500, blank= True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob = models.DateField(blank=True)
    city=models.CharField(max_length=50, validators=[commissionerfvalidation])
    
    def __str__(self):
        return self.firstname

class inspector(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50, validators =[validation])
    lastname = models.CharField(max_length=50, validators =[lastname_validation])
    profile_pic=models.FileField(upload_to='images/',default='default-pic.png')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format of intergers only . Up to 10 digits allowed.")
    contact_no=models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    address = models.CharField(max_length= 500, blank= True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob = models.DateField(blank=True)
    area=models.CharField(max_length=50)
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    def __str__(self):
        return self.firstname
        
class law(models.Model):
    law_title = models.CharField(max_length=500)
    law_summary = models.CharField(max_length=500)
    law_rules1 = models.CharField(max_length=200)
    law_rules2 = models.CharField(max_length=200)
    law_rules3 = models.CharField(max_length=200)
    law_rules4 = models.CharField(max_length=200)
    law_rules5 = models.CharField(max_length=200)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)
    law_icon = models.CharField(max_length= 500, blank= True)

    def __str__(self):
        return self.law_title
        
class crime_category(models.Model):
    cat_img=models.FileField(upload_to='images/',null=True,blank=True,default='default-pic.png')
    crime_category_name= models.CharField(max_length=500)

    def __str__(self):
        return self.crime_category_name
    

class Sub_crime(models.Model):
    crime_id=models.ForeignKey(crime_category, on_delete = models.CASCADE)
    sub_category_name= models.CharField(max_length=100)
    
    def __str__(self):
        return self.sub_category_name

class complaint(models.Model):
    firstname = models.CharField(max_length=50, validators=[commissionerfvalidation])
    lastname = models.CharField(max_length=50, validators=[commissionerlvalidation])
    citizen_id=models.ForeignKey(citizen, on_delete = models.CASCADE)
    complaint_title=models.CharField(max_length=50)
    complaint_description=models.CharField(max_length=500)
    complaint_no=models.CharField(max_length=100)
    proof_img=models.FileField(upload_to='images/',null=True,blank=True)
    proof_video=models.FileField(upload_to='videos/',null=True,verbose_name="video file",blank=True)
    gender = models.CharField(max_length=10)
    dob = models.DateField(blank=False)
    pname = models.CharField(max_length=100, validators =[lastname_validation])
    complaint_date=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.complaint_no

class policestation(models.Model):
    inspector_id = models.ForeignKey(inspector, on_delete = models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format of intergers only . Up to 10 digits allowed.")
    policestation_contact_no=models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    policestation_address = models.CharField(max_length= 500, blank= True)
    policestation_area=models.CharField(max_length=50)
    policestation_city=models.CharField(max_length=50, validators =[lastname_validation])
    policestation_name = models.CharField(max_length=100, validators =[lastname_validation])

    def __str__(self):
        return self.policestation_name


class FIR(models.Model):
    citizen_id=models.ForeignKey(citizen, on_delete = models.CASCADE)
    crime_id=models.ForeignKey(crime_category, on_delete = models.CASCADE)
    policestation_id = models.ForeignKey(policestation, on_delete = models.CASCADE)
    subcrime_id=models.ForeignKey(Sub_crime,on_delete= models.CASCADE)
    FIR_no=models.CharField(max_length=100)
    firstname = models.CharField(max_length=50, validators=[commissionerfvalidation])
    lastname = models.CharField(max_length=50, validators=[commissionerlvalidation])
    proof_img=models.FileField(upload_to='images/',null=True,blank=True)
    proof_video=models.FileField(upload_to='videos/',null=True,verbose_name="video file",blank=True)
    gender = models.CharField(max_length=10)
    dob = models.DateField(blank=False)
    FIR_date=models.DateTimeField(default=timezone.now)
    email = models.CharField( max_length = 200, validators =[validate_geeks_mail]) 
    FIR_description=models.CharField(max_length=500)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered in the format of intergers only . Up to 10 digits allowed.")
    contact_no=models.CharField(validators=[phone_regex], max_length=10, blank=True) # validators should be a list
    status=models.CharField(max_length=10,default="PENDING")

    def __str__(self):
        return self.FIR_no

class feedback(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    citizen_id=models.ForeignKey(citizen, on_delete = models.CASCADE)
    ratings=models.IntegerField(max_length=10,blank=False)
    feedback_desc=models.CharField(max_length=1000,default="")
    feedback_date= models.DateTimeField(default=timezone.now)

    


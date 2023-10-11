from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
import datetime

SALUTATION_CHOICES = [
    ('Mr.','Mr.'),
    ('Mrs.','Mrs.'),
    ('Miss','Miss'),
    ('Master','Master')
]

GENDER_CHOICES = [
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
]

VISATYPE_CHOICES = [
    ('Single','Single'),
    ('Couple','Couple'),
    ('Family','Family')
]

TYPE_CHOICES = [
    ('Appointment','Appointment'),
    ('Contact Us','Contact Us')
]   


class VisaCountry(models.Model):
    country = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    archive = models.BooleanField(default=False)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "VisaCountry"

    def __str__(self):
        return self.country
    

class VisaCategory(models.Model):
    visa_country_id = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)    
    category = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = "VisaCategory"

    def __str__(self):
        return self.category
    


class VisaSubcategory(models.Model):
    country_id = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)
    category_id = models.ForeignKey(VisaCategory,on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=100)
    estimate_amt = models.FloatField()
    cgst = models.FloatField()
    sgst = models.FloatField()
    totalAmount = models.FloatField()
    status = models.BooleanField(default=True)
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "Subcategory"

    def __str__(self):
        return self.subcategory_name
    
    
class Department(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"


class CustomUser(AbstractUser):
    user_type_data=(('1',"HOD"),('2',"Admin"),('3',"Employee"),('4',"Agent"),('5',"Out Sourcing Agent"),('6',"Customer"))
    user_type=models.CharField(default='1',choices=user_type_data,max_length=10)
    is_logged_in = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Admin(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=10)

    def __str__(self):
        return self.users.first_name
    


class CourierAddress(models.Model):
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class CaseStatus(models.Model):
    case_status = models.CharField(max_length=100)
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "CaseStatus"


class followuppayment_status(models.Model):
    followup_status = models.CharField(max_length=200)
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "Followup Payment Status"


class followup_status(models.Model):
    followup_status = models.CharField(max_length=200)
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "Followup Status"

class followupType(models.Model):

    followup_type = models.CharField(max_length=200)
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "Followup Type"


class DocumentCategory(models.Model):
    Document_category = models.CharField(max_length=200)
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Document_category
    
    
 
class CaseCategoryDocument(models.Model):
    country = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)
    category = models.ForeignKey(VisaCategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(VisaSubcategory,on_delete=models.CASCADE)
    digitalphoto = models.BooleanField(default=False)
    passportback = models.BooleanField(default=False)
    passportfront = models.BooleanField(default=False)
    pancard = models.BooleanField(default=False)
    adharcard = models.BooleanField(default=False)
    gapmonth = models.BooleanField(default=False)
    experience_letter = models.BooleanField(default=False)
    gapyear = models.BooleanField(default=False)
    masterscertificate = models.BooleanField(default=False)
    form16 = models.BooleanField(default=False)
    spouse = models.BooleanField(default=False)
    itr = models.BooleanField(default=False)
    spouseworking = models.BooleanField(default=False)
    spouseenglish = models.BooleanField(default=False)
    bankbalance = models.BooleanField(default=False)
    itr3years = models.BooleanField(default=False)
    evidenceofsalary = models.BooleanField(default=False)
    assetsdocument = models.BooleanField(default=False)
    marriagecertificate = models.BooleanField(default=False)
    spousequalification = models.BooleanField(default=False)
    bankbalance6month = models.BooleanField(default=False)
    workexperience = models.BooleanField(default=False)
    applicantsbankbalance = models.BooleanField(default=False)
    parentbankbalance = models.BooleanField(default=False)
    graduation_diploma = models.BooleanField(default=False)
    parentsid = models.BooleanField(default=False)
    parentsitr = models.BooleanField(default=False)
    englishlanguage = models.BooleanField(default=False)
    studentsbank = models.BooleanField(default=False)
    parentbank = models.BooleanField(default=False)
    parentdocument = models.BooleanField(default=False)
    passport = models.BooleanField(default=False)
    idproof = models.BooleanField(default=False)
    certificate_12th = models.BooleanField(default=False)
    certificate_10th = models.BooleanField(default=False)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.country} - {self.category} - {self.subcategory}"

class Group(models.Model):
    group_name = models.CharField(max_length=100, unique=True)
    group_member = models.ManyToManyField(CustomUser, related_name='groups_member')
    create_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_name   

class Currency(models.Model):
    currency_name = models.CharField(max_length=200)
    currency_rate = models.IntegerField()
    status = models.BooleanField()
    lastupdated_by = models.CharField(max_length=100,null=True,blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = "Currency"

    
class SuccessStories(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(max_length=100)
    image = models.FileField(upload_to="media/general/successstories",null=True,blank=True)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
 
NEWSTYPE_CHOICES = [
    ('For Dashboard','For Dashboard'),
    ('For FrontWebsite','For FrontWebsite')
]
    
class News(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    publish_date = models.DateField(auto_created=False)
    expiry_date = models.DateField(auto_created=False)
    news_type = models.CharField(max_length=50,choices=NEWSTYPE_CHOICES,default='Select News')
    status = models.BooleanField()
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class OfferBanner(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=50)
    fromdate = models.DateField(auto_created=False)
    todate = models.DateField(auto_created=False)
    image = models.FileField(upload_to="media/general/offerbanner")
    status = models.BooleanField()
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Branch(models.Model):
    branch_name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.branch_name


class Employee(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True)
    department = models.ForeignKey(to=Department,on_delete=models.SET_NULL,null=True, blank=True)
    contact_no = models.CharField(max_length=20,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    City = models.CharField(max_length=50,null=True,blank=True)
    Address = models.TextField(null=True,blank=True)
    zipcode = models.CharField(max_length=100,null=True,blank=True)
    status = models.BooleanField(null=True,blank=True)
    file = models.ImageField(upload_to="media/Employee/profile_pic/",null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    

type = [
    ('Outsourcing partner','Outsourcing partner'),
    ('Agent','Agent'),

]

class Package(models.Model):
    visa_country = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)
    visa_category = models.ForeignKey(VisaCategory,on_delete=models.CASCADE)
    visa_subcategory = models.ForeignKey(VisaSubcategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    assign_to_group = models.ForeignKey(Group,on_delete=models.CASCADE)
    number_of_visa = models.IntegerField()
    amount = models.FloatField()
    advance_amount = models.FloatField()
    file_charges = models.FloatField()
    image = models.FileField(upload_to='media/package/')
    word_doc = models.FileField(upload_to='media/package/worddoc/')
    package_expiry_date = models.DateField(auto_created=False)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class FrontWebsiteEnquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    appointment_date = models.DateTimeField(auto_created=False,null=True,blank=True)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='Appointment',null=True,blank=True)
    country_name = models.ForeignKey(VisaCountry,on_delete=models.CASCADE,null=True,blank=True)
    category_name = models.ForeignKey(VisaCategory,on_delete=models.CASCADE,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to="media/frontwebsiteenquiry/",null=True,blank=True)
    last_updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name    


type = [
    ('Outsourcing partner','Outsourcing partner'),
    ('Agent','Agent'),

]

status = [
    ('Pending','Pending'),
    ('InReview','InReview'),
    ('Approved','Approved'),
    ('Reject','Reject'),
]



class Agent(models.Model):
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)  
    type = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.TextField()
    zipcode = models.CharField(max_length=100)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=255,choices=status,default='Pending')
    activeinactive=models.BooleanField()
    profile_pic = models.ImageField(upload_to="media/Agent/Profile Pic/")


    organization_name = models.CharField(max_length=100,null=True,blank=True)
    business_type = models.CharField(max_length=100,null=True,blank=True)
    registration_number = models.CharField(max_length=100,null=True,blank=True)

    # ---------- Bank Information ---------------- 

    account_holder = models.CharField(max_length=100,null=True,blank=True)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    account_no = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    registeron = models.DateTimeField(auto_now_add=True, auto_now=False)
    registerdby = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_agents')

    # -------------------------- kyc information ------------------ 

    adhar_card_front = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    adhar_card_back = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    pancard = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    registration_certificate = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    


class OutSourcingAgent(models.Model):
    
    
    users = models.OneToOneField(CustomUser,on_delete=models.CASCADE)  
    type = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    City = models.CharField(max_length=50)
    Address = models.TextField()
    zipcode = models.CharField(max_length=100)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=10,null=True,blank=True)
    status = models.CharField(max_length=255,choices=status,default='Pending')
    activeinactive=models.BooleanField()
    profile_pic = models.ImageField(upload_to="media/OutSourcing/Agent/Profile Pic/")


    organization_name = models.CharField(max_length=100,null=True,blank=True)
    business_type = models.CharField(max_length=100,null=True,blank=True)
    registration_number = models.CharField(max_length=100,null=True,blank=True)

    # ---------- Bank Information ---------------- 

    account_holder = models.CharField(max_length=100,null=True,blank=True)
    bank_name = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    account_no = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    registeron = models.DateTimeField(auto_now_add=True, auto_now=False)
    registerdby = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='registered_outsourcingagents')


    # -------------------------- kyc information ------------------ 

    adhar_card_front = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    adhar_card_back = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    pancard = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    registration_certificate = models.FileField(upload_to="media/Agent/Kyc",null=True,blank=True)
    


leads_status = [
    ('New Lead','New Lead'),
    ('PreEnrolled','PreEnrolled'),
    ('Pending','Pending'),
    ('Accept','Accept'),
    ('Reject','Reject'),
    ('Archive','Archive'),
    ('Case Initiated','Case Initiated'),
]


class Enquiry(models.Model):
   
    
    Salutation = models.CharField(max_length=20,choices=SALUTATION_CHOICES) 
    FirstName = models.CharField(max_length=50)
    MiddleName = models.CharField(max_length=50,null=True,blank=True)
    LastName = models.CharField(max_length=50)
    Dob = models.DateField()
    Gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=100,null=True,blank=True)
    
    Visa_country = models.ForeignKey(VisaCountry,on_delete=models.CASCADE)
    Visa_category = models.ForeignKey(VisaCategory,on_delete=models.CASCADE)
    Visa_subcategory = models.ForeignKey(VisaSubcategory,on_delete=models.CASCADE)


    Visa_type = models.CharField(max_length=50,choices=VISATYPE_CHOICES)
    Package = models.ForeignKey(Package,on_delete=models.CASCADE)
    Source = models.CharField(max_length=100,null=True,blank=True)
    Reference = models.CharField(max_length=100,null=True,blank=True)
    lead_status = models.CharField(max_length=100,choices=leads_status,default="New Lead")
    # manage_status = models.CharField(max_length=100,choices=manage_status,default="Pending")
    enquiry_number = models.CharField(max_length=10, unique=True)
    assign_to_employee = models.ForeignKey(Employee,on_delete=models.SET_NULL,null=True,blank=True)
    assign_to_agent = models.ForeignKey(Agent,on_delete=models.SET_NULL,null=True,blank=True)
    assign_to_outsourcingagent = models.ForeignKey(OutSourcingAgent,on_delete=models.SET_NULL,null=True,blank=True)





    # Mailing Address
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=10)
    Country = CountryField()
    # Country = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    zipcode = models.CharField(max_length=255,null=True,blank=True)
    address= models.TextField(null=True,blank=True)


   
    #permanent address details 

    permanent_country = models.CharField(max_length=244,null=True,blank=True)
    permanent_state = models.CharField(max_length=100,null=True,blank=True)
    permanent_city = models.CharField(max_length=100,null=True,blank=True)
    permanent_zipcode = models.CharField(max_length=100,null=True,blank=True)
    permanent_address = models.TextField(null=True,blank=True)
    
    #passport information

    passport_no = models.CharField(max_length=255,null=True,blank=True)
    issue_date = models.DateField(null=True,blank=True)
    expirty_Date = models.DateField(null=True,blank=True)
    issue_country = models.CharField(max_length=255,null=True,blank=True)
    city_of_birth = models.CharField(max_length=100,null=True,blank=True)
    country_of_birth = models.CharField(max_length=244,null=True,blank=True)

    #Nationality Information
    nationality = models.CharField(max_length=100,null=True,blank=True)
    citizenship = models.CharField(max_length=100,null=True,blank=True)
    more_than_country = models.BooleanField(null=True,blank=True)
    other_country = models.BooleanField(null=True,blank=True)
    more_than_one_country = models.CharField(max_length=100,null=True,blank=True)
    studyin_in_other_country = models.CharField(max_length=100,null=True,blank=True)

    # Emergency Contact
    emergency_name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    emergency_email = models.EmailField(null=True,blank=True)
    relation_With_applicant = models.CharField(max_length=100,null=True,blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    registered_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    case_id = models.CharField(max_length=15, unique=True, editable=False) 
    case_status = models.ForeignKey(CaseStatus,on_delete=models.SET_NULL,null=True,blank=True)


    def generate_case_id(self):
        # Get the current date
        current_date = datetime.date.today()
        
        # Get the current month abbreviation (e.g., 'SEP' for September)
        current_month_abbrev = current_date.strftime('%b').upper()
        
        # Get the current day as a two-digit string (e.g., '25' for the 25th day)
        current_day = current_date.strftime('%d')
        
        # Generate a unique serial number (e.g., '00001')
        serial_number = self.get_next_serial_number()
        
        # Combine all components to form the case_id
        self.case_id = f'{current_month_abbrev}{current_day}-{serial_number}'

    def get_next_serial_number(self):
        # Calculate the next serial number based on existing records
        last_enquiry = Enquiry.objects.order_by('-id').first()
        if last_enquiry and last_enquiry.case_id:
            last_serial_number = int(last_enquiry.case_id.split('-')[1])
            next_serial_number = last_serial_number + 1
        else:
            next_serial_number = 1
        
        # Format the serial number as a zero-padded string (e.g., '00001')
        return f'{next_serial_number:05d}'
    

    class Meta:
        db_table = "Enquiry"

    def save(self, *args, **kwargs):
        if not self.enquiry_number:
            # Find the highest existing enquiry number and increment it
            highest_enquiry = Enquiry.objects.order_by('-enquiry_number').first()
            if highest_enquiry:
                last_enquiry_number = int(highest_enquiry.enquiry_number)
                self.enquiry_number = str(last_enquiry_number + 1)
            else:
                # If no existing enquiries, start with 100
                self.enquiry_number = "100"
        if not self.case_id:
            self.generate_case_id()

        super(Enquiry, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.email


class Document(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.SET_NULL,null=True,blank=True)
    document_name = models.CharField(max_length=255)
    document_category = models.ForeignKey(DocumentCategory,on_delete=models.CASCADE)
    document_size = models.FloatField()
    document_file = models.FileField(upload_to="media/Documents/",null=True,blank=True)
    status = models.BooleanField()
    lastupdated_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.document_name
   

class Notes(models.Model):
    enquiry = models.ForeignKey(Enquiry,on_delete=models.SET_NULL,null=True,blank=True)
    notes = models.CharField(max_length=255)
    file = models.FileField(upload_to='media/Notes/',null=True,blank=True)
    ip_address = models.GenericIPAddressField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_date= models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Notes"
        
    def __str__(self):
        return self.notes

class Education_Summary(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE,null=True,blank=True)
    country_of_education = models.CharField(max_length=100,null=True,blank=True)
    highest_level_education = models.CharField(max_length=100,null=True,blank=True)
    grading_scheme = models.CharField(max_length=100,null=True,blank=True)
    grade_avg = models.CharField(max_length=100,null=True,blank=True)
    recent_college = models.BooleanField(null=True,blank=True)
    level_education = models.CharField(max_length=100,null=True,blank=True)
    country_of_institution = models.CharField(max_length=100,null=True,blank=True)
    name_of_institution = models.CharField(max_length=100,null=True,blank=True)
    primary_language = models.CharField(max_length=100,null=True,blank=True)
    institution_from = models.DateField(null=True,blank=True)
    institution_to = models.DateField(null=True,blank=True)
    degree_Awarded = models.CharField(max_length=100,null=True,blank=True)
    degree_Awarded_On = models.CharField(max_length=100,null=True,blank=True)
    Address = models.CharField(max_length=255,null=True,blank=True)
    city = models.CharField(max_length=255,null=True,blank=True)
    Province = models.CharField(max_length=100,null=True,blank=True)
    zipcode = models.IntegerField(null=True,blank=True)



exam_type = [
    ('PTE','PTE'),
    ('TOEFL','TOEFL'),
    ('IELTS','IELTS'),
    
]



class TestScore(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE,null=True,blank=True)
    # candidates_name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=100,choices=exam_type)
    exam_date = models.DateField()
    reading = models.IntegerField()
    listening = models.IntegerField()
    speaking = models.IntegerField()
    writing = models.IntegerField()
    overall_score = models.IntegerField()

class Background_Information(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE)    
    background_information = models.CharField(max_length=244)


class ApplicationDocuments(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    comments = models.TextField()
    upload_documents = models.FileField(upload_to="media/Documents",null=True,blank=True)
     

class ApplicationStatus(models.Model):
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.CASCADE)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    updated_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)


class LoginLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    platform = models.CharField(max_length=200,default="Web")
    ip_address = models.GenericIPAddressField()
    login_datetime = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    # date = models.DateField()

    def save(self, *args, **kwargs):
        # Format the date and time as "13-Sep-2023 01:56 PM"
        formatted_datetime = self.login_datetime.strftime('%d-%b-%Y %I:%M %p')
        self.login_datetime_formatted = formatted_datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.login_datetime}"


class Appointment(models.Model):
    
    enquiry_id = models.ForeignKey(Enquiry,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=100)
    motive = models.CharField(max_length=100)
    date = models.DateField()
    time =models.TimeField()
    is_paid = models.BooleanField()
    amount = models.IntegerField()
    paid_amt = models.IntegerField()
    notes = models.TextField()
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to="media/upload to/",null=True,blank=True)


@receiver(post_save,sender=CustomUser)
def create_admin_profile(sender,instance,created, **kwargs):
    # if instance.user_type==''
    if created:
        if instance.user_type == '2':
            Admin.objects.create(users=instance, contact_no='')
        elif instance.user_type == '3':  # Check if the user type is 'ManPower'
            branch = Branch.objects.get(id=1)
            Employee.objects.create(users=instance, contact_no='',zipcode='',status='True',file='',branch=branch)
    
        elif instance.user_type == '4':  # Check if the user type is 'ManPower'
            Agent.objects.create(users=instance, contact_no='',zipcode='',activeinactive='True',type='',profile_pic='')
    
        elif instance.user_type == '5':  # Check if the user type is 'ManPower'
            OutSourcingAgent.objects.create(users=instance, contact_no='',zipcode='',activeinactive='True',type='',profile_pic='')
    

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type=='2':
        instance.admin.save()
    if instance.user_type=='3':
        instance.employee.save()
    if instance.user_type=='4':
        instance.agent.save()
    if instance.user_type=='5':
        instance.outsourcingagent.save()



MENU_CHOICES = [
        # ('Dashboard', 'Dashboard'),
        # ('Enquiry', 'Enquiry'),
        # ('Application Management', 'Application Management'),
        # ('Employee Management', 'Employee Management'),
        # ('Master Module', 'Master Module'),
        # ('Add Questions', 'Add Questions'),
        # ('Roles Management', 'Roles Management'),
        # ('Edit Client', 'Edit Client'),
        # ('Client Profile', 'Client Profile'),
        # ('Profile', 'Profile'),
        # ('View Employee', 'View Employee'),
        # ('General', 'General'),
        ('Add Leads', 'Add Leads'),
        # ('Agent Management', 'Agent Management'),
        # ('Personal Detail', 'Personal Detail'),
        # ('Commission Management', 'Commission Management'),
        # ('Add Commission', 'Add Commission'),
        # ('Commission', 'Commission'),
        # ('Add Follow up', 'Add Follow up'),
        # ('Follow ups', 'Follow ups'),
        # ('Packages', 'Packages'),
        # ('View Notification', 'View Notification'),
        # ('Chatting', 'Chatting'),
        # ('Chat', 'Chat'),
        # ('Settings', 'Settings'),
        # ('Add Appointment', 'Add Appointment'),
        # ('View Appointment', 'View Appointment'),
        # ('Update Case Status', 'Update Case Status'),
        ('Add Enquiry', 'Add Enquiry'),
        # ('Report', 'Report'),
        # ('Appointments', 'Appointments')
    ]        
        


class Menu(models.Model):
    name = models.CharField(max_length=255, choices=MENU_CHOICES)        

    def __str__(self):
        return self.name
    


class AssignRoles(models.Model):
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    menu_name = models.ManyToManyField(Menu)
    employee = models.ManyToManyField(Employee)


class AgentAgreement(models.Model):
    agent = models.ForeignKey(Agent,on_delete=models.SET_NULL,null=True,blank=True )    
    outsourceagent = models.ForeignKey(OutSourcingAgent,on_delete=models.SET_NULL,null=True,blank=True )    
    agreement_name = models.CharField(max_length=100)    
    agreement_file = models.FileField(upload_to="media/Agreement/",null=True,blank=True)


class IndividualMessage(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)    
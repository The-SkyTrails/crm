from django.contrib.auth import authenticate,logout, login as auth_login
import requests
from datetime import date
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View
from django.views.generic import CreateView , ListView , UpdateView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.core.files.storage import FileSystemStorage
from .models import UploadedFile
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpRequest


# def employee_dashboard(request):
#     user = request.user
#     assign_roles = AssignRoles.objects.filter(employee=user.employee)
#     menu_flags = {
#         "dashboard": False,
#         "add_lead": False,
#         "add_enquiry": False,
#         # Add more menu items and their flags as needed
#     }
#     # for assing in assign_roles:
#     #     print(assing.menu_name)
#     for assign in assign_roles:
#         print("sss",assign.menu_name.all())
#         for menu_item in assign.menu_name.all():
#             if menu_item == "add_enquiry":
#                 menu_flags["add_enquiry"] = True
#             elif menu_item == "Add Lead":
#                 menu_flags["add_lead"] = True
#             # Add more conditions for other menu items and flags as needed

#     context = {
#         "menu_flags": menu_flags
#     }

#     return render(request,'Employee/Base/index2.html',context)


# def employee_dashboard(request):
#     user = request.user
#     assign_roles = AssignRoles.objects.filter(employee=user.employee)
#     employee = Employee.objects.get(users=request.user)
#     asgn_rol = AssignRoles.objects.get(employee=request.user.employee)

#     print("ddddd",asgn_rol.menu_name.all())
        
#     if employee.department.name == "HR":
#         print("working")
#     else:
#         print("not working")
#         # print("herrr",HR)
    
#     print("helloo ss",employee)
#     menu_flags = {
#         "dashboard": False,
#         "add_lead": False,
#         "add_enquiry": False,
#         # Add more menu items and their flags as needed
#     }

#     for assign in assign_roles:
#         for menu_item in assign.menu_name.all():
#             if menu_item.name == "add_enquiry":
#                 menu_flags["add_enquiry"] = True
#             elif menu_item.name == "Add Lead":
#                 menu_flags["add_lead"] = True
#             # Add more conditions for other menu items and flags as needed

#     context = {
#         "menu_flags": menu_flags,
#         "employee":employee,
#         "asgn_rol":asgn_rol
        
        
#     }

#     return render(request, 'Employee/Base/index2.html', context)


from django.core.exceptions import ObjectDoesNotExist
def employee_dashboard(request):
    user = request.user
    try:
        asgn_rol = AssignRoles.objects.get(employee=user.employee)
    except ObjectDoesNotExist:
        # Handle the case where no assignment exists for the user
        asgn_rol = None

    employee = Employee.objects.get(users=request.user)

    if employee.department.name == "HR":
        print("working")
    else:
        print("not working")
    
    menu_flags = {
        "dashboard": False,
        "add_lead": False,
        "add_enquiry": False,
        # Add more menu items and their flags as needed
    }

    # for assign in assign_roles:
    #     for menu_item in assign.menu_name.all():
    #         if menu_item.name == "add_enquiry":
    #             menu_flags["add_enquiry"] = True
    #         elif menu_item.name == "Add Lead":
    #             menu_flags["add_lead"] = True
            # Add more conditions for other menu items and flags as needed

    context = {
        "menu_flags": menu_flags,
        "employee": employee,
        "asgn_rol": asgn_rol
    }

    return render(request, 'Employee/Base/index2.html', context)

def employee_logout(request):
    logout(request)
    return redirect("employee_login")

def employee_login(request):
    error_message = None  

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
                auth_login(request, user)
                print("Logged in successfully")
                return redirect('employee_dashboard')  # Redirect to the common dashboard
        else:
            error_message = "Username or password is incorrect."

    return render(request, 'Employee/LoginPage/newlogin.html', {'error_message': error_message})


class EmployeeEnquiryCreateView(CreateView):

    model = Enquiry
    form_class = EnquiryForm
    template_name = 'Employee/Leads/addenquiry.html'
    success_url = reverse_lazy('employee_leads') 
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.assign_to_employee = self.request.user.employee
        form.instance.lead_status = "PreEnrolled"
        messages.success(self.request, 'Enquiry Added Successfully.')
        return super().form_valid(form) 



def employee_leads(request):
    user = request.user
    created_enq = Enquiry.objects.filter(created_by=user)
    if user.is_authenticated:
        # Check if the user is an Agent or Outsourcing Agent
        if user.user_type == '3':
            # If the user is an Agent, filter by assign_to_agent
            enq = Enquiry.objects.filter(Q(assign_to_employee=user.employee))
            print("helooooo",user)
        else:
            # Handle other user types as needed
            enq = None
        combined_enq = enq | created_enq

        print("enquiry", combined_enq)

        return render(request, 'Employee/Leads/leads.html', {'enq': combined_enq})


def viewemployee_enqlist(request,id):
    enq = Enquiry.objects.get(id=id)
    context={
        "enq":enq
    }
    return render(request,'Employee/Leads/viewenquiry.html',context) 


def employee_accept_leads(request):
    if request.method == "POST":
        accept = request.POST.get('accept')
        print("accepptt",accept)
        enq_id = request.POST.get('enq_id')
        enquiry = Enquiry.objects.get(id=enq_id)
        enquiry.lead_status = "PreEnrolled"
        enquiry.assign_to_employee=request.user.employee
        enquiry.save()
        return redirect('employee_leads')
    
    
class MenuListView(ListView):
    model = Menu
    template_name = 'Employee/Rolesmanagement/menulist.html'
    context_object_name = 'menu'


class AddMenu(CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'Employee/Rolesmanagement/addmenu.html'
    success_url = reverse_lazy('Employee_Menu_list')  
    
    def form_valid(self, form):
        # Check if a menu item with the same name already exists
        name = form.cleaned_data['name']
        if Menu.objects.filter(name=name).exists():
            # Handle the case where the menu item already exists
            # You can add your custom logic here, such as showing an error message
            # or redirecting to a different page
            messages.warning(self.request, 'Menu item with this name already exists.')
            return redirect('Employee_add_menu')

        # If the menu item doesn't exist, proceed with saving it
        messages.success(self.request, 'Menu item has been successfully created.')
        return super().form_valid(form)

class EditMenuView(LoginRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'Employee/Rolesmanagement/menuupdate.html'
    success_url = reverse_lazy('Employee_Menu_list')

    def form_valid(self, form):
        # Check if a menu item with the same name already exists
        name = form.cleaned_data['name']
        menu_instance = self.get_object()

        if Menu.objects.exclude(pk=menu_instance.pk).filter(name=name).exists():
            # Handle the case where the menu item already exists
            # You can add your custom logic here, such as showing an error message
            # or redirecting to a different page
            messages.warning(self.request, 'Menu item with this name already exists.')
        else:
            # If the menu item doesn't exist, proceed with saving it
            messages.success(self.request, 'Menu item has been updated successfully.')
            response = super().form_valid(form)
            return redirect(self.get_success_url())

        # Redirect back to the form page
        return redirect(self.get_success_url())     
    
    
def add_employee(request):
    departments = Department.objects.all()
    branches = Branch.objects.all()

    if request.method == "POST":
        department_id = request.POST.get('department_id')
        branch_id = request.POST.get('branch_id')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        status = request.POST.get('status')
        files = request.FILES.get('file')

        # Ensure that branch_id is provided
        if not branch_id:
            messages.warning(request, 'Branch ID is required')
            return redirect('Employee_add_employee')

        try:
            department = Department.objects.get(id=department_id)
            branchh = Branch.objects.get(id=branch_id)
            user = CustomUser.objects.create_user(
                username=email, first_name=firstname, last_name=lastname, email=email, password=password, user_type='3'
            )
           
            user.employee.department = department
            user.employee.branch = branchh
            user.employee.contact_no = contact
            user.employee.country = country
            user.employee.state = state
            user.employee.City = city
            user.employee.Address = address
            user.employee.zipcode = zipcode
            user.employee.status = status
            user.employee.file = files
            user.save()
            messages.success(request, 'Employee Added Successfully!!')
            return redirect('Employee_all_employee')
        except Exception as e:
            messages.warning(request, str(e))
            return redirect('Employee_add_employee')

    context = {
        'department': departments,
        'branch': branches
    }
    return render(request, 'Employee/Employee/addemployee.html', context)


class all_employee(ListView):
    model = Employee
    template_name = 'Employee/Employee/employeelist.html'  
    context_object_name = 'employee'
    

class view_employee(ListView):
    model = Employee
    template_name = 'Employee/Employee/employeeview.html'  
    context_object_name = 'employee'
    
    def get_queryset(self):
        # Get the employee_id from the URL parameter
        employee_id = self.kwargs['employee_id']
        
        
        # Filter the queryset to get the employee with the specified ID
        queryset = Employee.objects.get(id=employee_id)
        
        
        return queryset
    

def employee_update(request,pk):
    department = Department.objects.all()
    employee = Employee.objects.get(pk=pk)
    context = {
        'employee':employee,
        'department':department,
    }

    return render(request,'Employee/Employee/employeeupdate.html',context)
    

def employee_update_save(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        department_id = request.POST.get('department')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        status = request.POST.get('status')
        file = request.FILES.get('file')
        

        
        user = CustomUser.objects.get(id=employee_id)
       
        department = Department.objects.get(id=department_id)

        user.first_name= firstname
        user.last_name= lastname
        user.email= email

        user.employee.department= department
       
        user.employee.contact_no=contact
        user.employee.country= country
        user.employee.state= state
        user.employee.City= city
        user.employee.Address= address
        user.employee.zipcode= zipcode
        user.employee.status= status
        if file:
            user.employee.file= file
        user.save()
        messages.success(request,'Employee Updated Successfully')
        return redirect("Employee_all_employee")
  
    
class SuccessStoriesCreateView(CreateView):
    model = SuccessStories
    form_class = SuccessStoriesForm
    template_name = 'Employee/general/SuccessStories/addnewsuccessstory.html'
    success_url = reverse_lazy('Employee_SuccessStories_list')  
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        
        messages.success(self.request, 'SuccessStory Added Successfully.')
          
        return super().form_valid(form)
    
    
class SuccessStoriesListView(ListView):
    model = SuccessStories
    template_name = 'Employee/general/SuccessStories/successstorieslist.html'  
    context_object_name = 'SuccessStories'


class editSuccessStory(LoginRequiredMixin,UpdateView):
    model = SuccessStories
    form_class = SuccessStoriesForm
    template_name = 'Employee/general/SuccessStories/updatesuccessstory.html'
    success_url = reverse_lazy('Employee_SuccessStories_list')

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, 'SuccessStory Updated Successfully.')

        return super().form_valid(form)
    
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'Employee/general/News/addnews.html'
    success_url = reverse_lazy('Employee_News_list')  
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        
        messages.success(self.request, 'News Added Successfully.')
          
        return super().form_valid(form)
    
    
class NewsListView(ListView):
    model = News
    template_name = 'Employee/general/News/newslist.html'  
    context_object_name = 'News'


class editNews(LoginRequiredMixin,UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'Employee/general/News/updatenews.html'
    success_url = reverse_lazy('Employee_News_list')

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, 'News Updated Successfully.')

        return super().form_valid(form)
    
    
class OfferBannerCreateView(CreateView):
    model = OfferBanner
    form_class = OfferBannerForm
    template_name = 'Employee/general/OfferBanner/addofferbanner.html'
    success_url = reverse_lazy('Employee_OfferBanner_list') 
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        
        messages.success(self.request, 'OfferBanner Added Successfully.')
          
        return super().form_valid(form)
    
    
class OfferBannerListView(ListView):
    model = OfferBanner
    template_name = 'Employee/general/OfferBanner/offerbannerlist.html'  
    context_object_name = 'OfferBanner'


class editOfferBanner(LoginRequiredMixin,UpdateView):
    model = OfferBanner
    form_class = OfferBannerForm
    template_name = 'Employee/general/OfferBanner/updateofferbanner.html'
    success_url = reverse_lazy('Employee_OfferBanner_list')

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, 'OfferBanner Updated Successfully.')

        return super().form_valid(form)
    
    
class PackageCreateView(CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'Employee/Package/addpackage.html'
    success_url = reverse_lazy('Employee_Package_list')  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visa_countries'] = VisaCountry.objects.all()
        context['visa_categories'] = VisaCategory.objects.all()
        context['visa_subcategories'] = VisaSubcategory.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        
        # Handle the Word document file upload here
        word_doc = self.request.FILES.get('word_doc')
        if word_doc:
            # Save the Word document to the appropriate directory
            form.instance.word_doc = word_doc
        
        messages.success(self.request, 'Package Added Successfully.')
        return super().form_valid(form)
    
    
class PackageListView(ListView):
    model = Package
    template_name = 'Employee/Package/packagelist.html'  
    context_object_name = 'Package'


class editPackage(LoginRequiredMixin,UpdateView):
    model = Package
    form_class = PackageForm
    template_name = 'Employee/Package/packageupdate.html'
    success_url = reverse_lazy('Employee_Package_list')

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, 'Package Updated Successfully.')

        return super().form_valid(form)
    
    
class FrontWebsiteEnquiryCreateView(CreateView):
    model = FrontWebsiteEnquiry
    form_class = FrontWebsiteEnquiryForm
    template_name = 'Employee/FrontWebsiteEnquiry/addenquiry.html'
    success_url = reverse_lazy('Employee_FrontWebsiteEnquiry_list') 
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['visa_countries'] = VisaCountry.objects.all()
    #     context['visa_categories'] = VisaCategory.objects.all()
    #     return context
    
    def form_valid(self, form):
        form.instance.last_updated_by = self.request.user
        user = self.request.user
        print("userrrrrrrrrrr",user)
        messages.success(self.request, 'FrontWebsiteEnquiry Added Successfully.')
        return super().form_valid(form)
    
    
class FrontWebsiteEnquiryListView(ListView):
    model = FrontWebsiteEnquiry
    template_name = 'Employee/FrontWebsiteEnquiry/FrontWebsiteEnquirylist.html'  
    context_object_name = 'FrontWebsiteEnquiry'


def view_frontenqlist(request,id):
    enq = FrontWebsiteEnquiry.objects.get(id=id)
    context={
        "enq":enq
    }
    return render(request,'Employee/FrontWebsiteEnquiry/viewfrontenquiry.html',context)      

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_public_ip():
        try:
            response = requests.get('https://api64.ipify.org?format=json')
            data = response.json()
            return data['ip']
        except Exception as e:
            # Handle the exception (e.g., log the error)
            return None


class enrolled_Application(ListView):
    model = Enquiry
    template_name = 'Employee/ApplicationManagement/EnrolledApplication/enrolledapplicationlist.html'  
    context_object_name = 'enquiry'

    def get_queryset(self):
        # Filter Enquiry objects with status "Accept"
        # return Enquiry.objects.filter(lead_status="Accept")
        return Enquiry.objects.filter(Q(lead_status="Accept") | Q(lead_status="Case Initiated"))


    def get_context_data(self, **kwargs):
        # Get the default context data (data from the Enquiry model)
        context = super().get_context_data(**kwargs)

        current_datetime = timezone.now()
        context['current_datetime'] = current_datetime
        
        # Add data from the Notes model to the context
        context['notes'] = Notes.objects.all()
        context['notes_first'] = Notes.objects.order_by('-id').first()
        # context['employee'] = Employee.objects.all()
        context['employee_queryset'] = Employee.objects.all()
        context['agent'] = Agent.objects.all()
        context['OutSourcingAgent'] = OutSourcingAgent.objects.all()
        
        # employee_queryset = Employee.objects.all()
       
        

        return context
      
    
def enrolled_add_notes(request):
    if request.method == "POST":
        enq_id = request.POST.get('enq_id')
        notes_text = request.POST.get('notes')
        file = request.FILES.get('file')
        user = request.user

        try:
            enq = Enquiry.objects.get(id=enq_id)
            ip_address = get_public_ip()
            
            # Get the client's IP address
            
            
            # Create the Notes instance with the Enquiry instance and IP address
            notes = Notes.objects.create(enquiry=enq, notes=notes_text, file=file, ip_address=ip_address, created_by=user)
            notes.save()
            
        except Enquiry.DoesNotExist:
            # Handle the case where the Enquiry with the given ID does not exist
            pass  # You can add appropriate error handling here if needed
    
    return redirect('Employee_enroll_application')

 
 
def assign_agent(request):
    if request.method == "POST":
        
        enq_id = request.POST.get('enq_id')
        lead_status = request.POST.get('lead_status')
        agent_id = request.POST.get('agent_id')

        enq = Enquiry.objects.get(id=enq_id)

        agent = Agent.objects.get(id=agent_id)
        enq.assign_to_agent = agent
        enq.save()


    return redirect('Employee_enroll_application')
 
def assign_outsourceagent(request):
    if request.method == "POST":
        enq_id = request.POST.get('enq_id')
        
        outsourceagent_id = request.POST.get('outsourceagent_id')

        enq = Enquiry.objects.get(id=enq_id)
        out_sourceagent = OutSourcingAgent.objects.get(id=outsourceagent_id)
        enq.assign_to_outsourcingagent = out_sourceagent
        enq.lead_status = "Case Initiated"
        enq.save()


    return redirect('Employee_enroll_application')



def assign_employee(request):
    if request.method == "POST":
        enq_id = request.POST.get('enq_id')
        lead_status = request.POST.get('lead_status')
        emp_id = request.POST.get('emp_id')

        enq = Enquiry.objects.get(id=enq_id)
        employee = Employee.objects.get(id=emp_id)
        enq.lead_status=lead_status
        enq.assign_to_employee = employee
        enq.save()


    return redirect('Employee_enroll_application')

def edit_enrolled_application(request,id):

    enquiry = Enquiry.objects.get(id=id)
    country = VisaCountry.objects.all()
    category = VisaCategory.objects.all()
    subcategory = VisaSubcategory.objects.all()
    context ={
        'enquiry':enquiry,
        'country':country,
        'category':category,
        'subcategory':subcategory,
    }
  
    return render(request,'Employee/ApplicationManagement/EnrolledApplication/editenrolledapplication.html',context)



def education_summary(request,id):
    
    enquiry = Enquiry.objects.get(id=id)
    # education_summary = Education_Summary.objects.get(enquiry_id=enquiry)
    if Education_Summary.objects.filter(enquiry_id=enquiry).exists():
        education_summary = Education_Summary.objects.get(enquiry_id=enquiry)
    else:
        # Handle the case where there is no matching Education_Summary
        education_summary = None 

    if request.method == "POST":
        enq_id = request.POST.get('enq_id')
        educationcountry = request.POST.get('educationcountry')
        highest_education = request.POST.get('highest_education')
        gradingscheme = request.POST.get('gradingscheme')
        gradeaverage = request.POST.get('gradeaverage')
        recent_college = request.POST.get('recent_college')
        level_education = request.POST.get('level_education')
        institutecountry = request.POST.get('institutecountry')
        institutename = request.POST.get('institutename')
        instructionlanguage = request.POST.get('instructionlanguage')
        institutionfrom = request.POST.get('institutionfrom')
        institutionto = request.POST.get('institutionto')
        degreeawarded = request.POST.get('degreeawarded')
        degreeawardedon = request.POST.get('degreeawardedon')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        zipcode = request.POST.get('zipcode')

        # education_summary = Education_Summary.objects.get(enquiry_id=enq_id)
        # education_summary, created = Education_Summary.objects.get_or_create(enquiry_id=enq_id)
        enquiry = get_object_or_404(Enquiry, id=enq_id)
        education_summary, created = Education_Summary.objects.get_or_create(enquiry_id=enquiry)
        education_summary.country_of_education =educationcountry
        education_summary.highest_level_education =highest_education
        education_summary.grading_scheme = gradingscheme
        education_summary.grade_avg = gradeaverage
        education_summary.recent_college = recent_college
        education_summary.level_education = level_education
        education_summary.country_of_institution = institutecountry
        education_summary.name_of_institution = institutename
        education_summary.primary_language = instructionlanguage
        education_summary.institution_from = institutionfrom
        education_summary.institution_to = institutionto
        education_summary.degree_Awarded = degreeawarded
        education_summary.degree_Awarded_On = degreeawardedon
        education_summary.Address = address
        education_summary.city = city
        education_summary.Province = province
        education_summary.zipcode = zipcode
        # education_summary.primary_language = institutecountry

        education_summary.save()
        return redirect('Employee_education_summary',id=id)
        

        # education_summary = Education_Summary.objects.create(enquiry_id=enq_id,country_of_education=educationcountry,highest_level_education=highest_education,grading_scheme=gradingscheme,grade_avg=gradeaverage,recent_college=recent_college)
    context = {
        'enquiry':enquiry,
        'education_summary':education_summary
    }
    return render(request,'Employee/ApplicationManagement/EnrolledApplication/Subforms/education-form.html',context)


def test_score(request, id):
    enquiry_id = Enquiry.objects.get(id=id)
    # education_summary = Education_Summary.objects.get(enquiry_id=enquiry)
    if TestScore.objects.filter(enquiry_id=enquiry_id).exists():
        test_score = TestScore.objects.get(enquiry_id=enquiry_id)
    else:
        # Handle the case where there is no matching Education_Summary
        test_score = None 
    
        
        
    if request.method == "POST":
            examtype = request.POST.get('examtype')
            examdate = request.POST.get('examdate')
            reading = request.POST.get('reading')
            listening = request.POST.get('listening')
            speaking = request.POST.get('speaking')
            writing = request.POST.get('writing')
            overallscore = request.POST.get('overallscore')

            # Check if a TestScore with the specified exam_type already exists
            existing_test_score = test_score.filter(exam_type=examtype).first()

            if existing_test_score is None:
                # If no TestScore with the specified exam_type exists, create a new one
                testScore = TestScore.objects.create(
                    enquiry_id=enquiry_id,
                    exam_type=examtype,
                    exam_date=examdate,
                    reading=reading,
                    listening=listening,
                    speaking=speaking,
                    writing=writing,
                    overall_score=overallscore
                )
                testScore.save()
            else:
                # If an existing TestScore with the same exam_type is found, update it
                existing_test_score.exam_date = examdate
                existing_test_score.reading = reading
                existing_test_score.listening = listening
                existing_test_score.speaking = speaking
                existing_test_score.writing = writing
                existing_test_score.overall_score = overallscore
                existing_test_score.save()
                
            return redirect('Employee_test_score', id=id)
    
    context = {
        'test_scores': test_score,
        'enquiry_id': enquiry_id,
    }
    return render(request, 'Employee/ApplicationManagement/EnrolledApplication/Subforms/test-score-form.html', context)


def edit_test_score(request,id):
    
    test_score = TestScore.objects.get(id=id)
    enquiry_id = test_score.enquiry_id.id
    test_scores = TestScore.objects.filter(enquiry_id=test_score.enquiry_id)
    if request.method == "POST":
        
        examtype = request.POST.get('examtype')
        examdate = request.POST.get('examdate')
        reading = request.POST.get('reading')
        listening = request.POST.get('listening')
        speaking = request.POST.get('speaking')
        writing = request.POST.get('writing')
        overallscore = request.POST.get('overallscore')

        test_score.exam_type = examtype
        test_score.exam_date = examdate
        test_score.reading = reading
        test_score.listening = listening
        test_score.speaking = speaking
        test_score.writing = writing
        test_score.overall_score = overallscore
        test_score.save()
        return redirect('Employee_test_score', id=enquiry_id)

   
    context = {
        "test_score":test_score,
        "test_scores":test_scores,
    }
   
   

   
    # return redirect('Employee_test_score', id=enquiry_id)
    return render(request,'Employee/ApplicationManagement/EnrolledApplication/Subforms/test_score_edit.html',context)


def delete_test_score(request,id):
    test_score = TestScore.objects.get(id=id)
    enquiry_id = test_score.enquiry_id.id
    test_score.delete()
    return redirect('Employee_test_score', id=enquiry_id)
    # print("sssss",test_score)

def background_information(request, id):
    enquiry_id = Enquiry.objects.get(id=id)
    
    try:
        # Try to retrieve an existing Background_Information entry for this enquiry
        bk_info = Background_Information.objects.get(enquiry_id=enquiry_id)
        
        if request.method == "POST":
            exaustralliabeforeamtype = request.POST.get('australliabefore')
            
            # Update the existing Background_Information entry
            bk_info.background_info = exaustralliabeforeamtype
            bk_info.save()
            
            return redirect('Employee_background_information', id=id)
    except Background_Information.DoesNotExist:
        # If no existing entry is found, create a new one
        bk_info = None
        
        if request.method == "POST":
            exaustralliabeforeamtype = request.POST.get('australliabefore')
            
            # Create a new Background_Information entry
            bk_info = Background_Information.objects.create(
                enquiry_id=enquiry_id,
                background_info=exaustralliabeforeamtype,
            )
            
            return redirect('Employee_background_information', id=id)
    
    context = {
        'bk_info': bk_info,
        'enquiry_id': enquiry_id,
    }
    return render(request, 'Employee/ApplicationManagement/EnrolledApplication/Subforms/background-form.html', context)

def documents(request,id):
    enquiry_id = Enquiry.objects.get(id=id)
    documents = ApplicationDocuments.objects.filter(enquiry_id=enquiry_id)
    context = {
        "enquiry_id":enquiry_id,
        "documents":documents,
    }
    return render(request, 'Employee/ApplicationManagement/EnrolledApplication/Subforms/document-form.html', context)


def create_documents(request,id):
    enquiry_id = Enquiry.objects.get(id=id)
    
    if request.method == "POST":
        documentname = request.POST.get('documentname')
        comment = request.POST.get('comment')
        files = request.FILES.get('files')
        documts = ApplicationDocuments.objects.create(enquiry_id=enquiry_id,document_name=documentname,comments=comment,upload_documents=files)
        documts.save()
    return redirect('Employee_documents',id=id)


def timeline(request,id):

    enquiry_id = Enquiry.objects.get(id=id)
    context = {
        "enquiry_id":enquiry_id
    }
    return render(request, 'Employee/ApplicationManagement/EnrolledApplication/Subforms/timeline-form.html', context)

def workexperience(request,id):
    enquiry_id = Enquiry.objects.get(id=id)
    context = {
        "enquiry_id":enquiry_id
    }
    return render(request, 'Employee/ApplicationManagement/EnrolledApplication/Subforms/workexperience-form.html', context)


# def upload_to(request):
    
def upload_to(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # Save the file to a temporary location (you can customize this)
        fs = FileSystemStorage(location='media/temp/')
        filename = fs.save(uploaded_file.name, uploaded_file)

        # Now, you can save the file's data to your database model
        uploaded_data = UploadedFile(file=filename)  # Adjust this according to your model
        uploaded_data.save()

        # Optionally, you can delete the temporary file
        fs.delete(filename)

        return redirect('/')  # Redirect to a success page

    # return render(request, 'upload.html')
    return render(request,'Employee/ApplicationManagement/upload_to.html')



##################### Visa Case #####################


   
class ClientList(ListView):
    model = Enquiry
    template_name = 'Employee/ApplicationManagement/VisaCases/visacaseslist.html'  
    context_object_name = 'enquiry'

    
    def get_queryset(self):
        # Filter Enquiry objects with status "Accept"
        # return Enquiry.objects.filter(lead_status="Accept")
        queryset = Enquiry.objects.filter(lead_status="Case Initiated")
        
        return queryset



def update_case_status(request,id):
    enq_id = Enquiry.objects.get(id=id)
    case_status = CaseStatus.objects.all()
    application_status = ApplicationStatus.objects.filter(enquiry_id=enq_id)
    
    if request.method == "POST":
        case_status_id = request.POST.get('case_status') 
        casestatus = CaseStatus.objects.get(id=case_status_id)
        enq_id.case_status=casestatus
        enq_id.save()
        appstatus = ApplicationStatus.objects.create(enquiry_id=enq_id,updated_by=request.user)

        appstatus.save()

    return render(request, 'Employee/ApplicationManagement/VisaCases/casestatus.html', {'enq_id': enq_id,'case_status':case_status,'application_status':application_status})

    # return redirect('Employee_update_case_status',id=id)


def client_documents(request):
    return render(request,'Employee/ApplicationManagement/UserDocument/adduserdocument.html')



def view_appointment(request,id):
    enq_id = Enquiry.objects.get(id=id)
    appointment = Appointment.objects.filter(enquiry_id=enq_id)
    context = {
        'enq_id':enq_id,
        'appointment':appointment,
    }
    return render(request,'Employee/ApplicationManagement/VisaCases/appointmentlist.html',context)


def add_appointment(request,id):
    enquiry = Enquiry.objects.get(id=id)
    if request.method == "POST":
        title = request.POST.get('title')
        motive = request.POST.get('motive')
        date = request.POST.get('date')
        time = request.POST.get('time')
        is_paid = request.POST.get('is_paid') == 'on'
        print("is paid", is_paid)
        
        amount = request.POST.get('amount')
        paid_amt = request.POST.get('paid_amount')
        
        notes = request.POST.get('notes')

        try:
            appointment = Appointment.objects.create(
                enquiry_id=enquiry, title=title, motive=motive, date=date,
                time=time, is_paid=is_paid, amount=amount, paid_amt=paid_amt, notes=notes
            )
            appointment.save()
            print("hello ggg")
            
            return redirect('Employee_view_appointment',id=id)  # Modify 'appointment_detail' to your URL pattern name
        except Exception as e:
            
            pass  


    return render(request,'Employee/ApplicationManagement/VisaCases/addappointment.html',{'enquiry':enquiry})


class loginlog(ListView):
    model = LoginLog
    template_name = 'Employee/General/Loginlogs/loginlogs.html'
    context_object_name = 'loginlog'

    
    def get_queryset(self):
        # Filter LoginLog entries where user_type is not equal to '1'
        return LoginLog.objects.exclude(user__user_type='1')
  


def search_loginlog(request):
    user = request.user
    if request.method == 'POST':
        
        
        # Check if the user_type is not '1' (HOD)
        if user.user_type != '1':
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            email = request.POST.get('user_id')
            user_type = request.POST.get('user_type')
            print("emailll",email)
            # Start with the full queryset
            loginlog_queryset = LoginLog.objects.all()

            # Exclude records with user_type = '1' (HOD)
            loginlog_queryset = loginlog_queryset.exclude(user__user_type='1')

            # Apply filters based on user input
            if from_date:
                # Filter by date if from_date is provided
               from_date_datetime = datetime.strptime(from_date, '%Y-%m-%d')
            #Make from_date_datetime timezone-aware
               from_date_aware = timezone.make_aware(from_date_datetime, timezone.get_current_timezone())
            # Filter by date if from_date is provided
               loginlog_queryset = loginlog_queryset.filter(login_datetime__date=from_date_aware.date())
            if to_date:
                to_date_datetime = datetime.strptime(from_date, '%Y-%m-%d')
                to_date_aware = timezone.make_aware(to_date_datetime, timezone.get_current_timezone())
                # Filter by date if to_date is provided
                loginlog_queryset = loginlog_queryset.filter(login_datetime__date=to_date_aware.date())
            if email:
                # Filter by name if name is provided
                loginlog_queryset = loginlog_queryset.filter(user__email__exact=email)
            if user_type:
                # Filter by name if name is provided
                loginlog_queryset = loginlog_queryset.filter(user__user_type__icontains=user_type)

            return render(request, 'Employee/General/Loginlogs/loginlogs.html', {'loginlog': loginlog_queryset})

    # If the request method is not POST or user_type is '1' (HOD), display all records except user_type '1'
    loginlog_queryset = LoginLog.objects.exclude(user__user_type='1')

    return render(request, 'Employee/General/Loginlogs/loginlogs.html', {'loginlog': loginlog_queryset})  

 
def add_agent(request):
    logged_in_user = CustomUser.objects.get(username=request.user.username)
    print(logged_in_user)
    if request.method == "POST":
        type = request.POST.get('type')
        # department = request.POST.get('department')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        activeinactive = request.POST.get('status')
        files = request.FILES.get('files')
       
        
        existing_agent= CustomUser.objects.filter(username=email)
        try:
            if existing_agent:
                messages.warning(request, f'"{email}" already exists.')
                return redirect('Employee_add_agent')
            if type == "Outsourcing Partner":
                user = CustomUser.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=password,user_type='5')
                logged_in_user = CustomUser.objects.get(username=request.user.username)
            
            
            # print("userssssssssss",users)
                user.outsourcingagent.type=type
                user.outsourcingagent.contact_no=contact
                user.outsourcingagent.country=country
                user.outsourcingagent.state=state
                user.outsourcingagent.City=city
                user.outsourcingagent.Address=address
                user.outsourcingagent.zipcode=zipcode
                user.outsourcingagent.activeinactive=activeinactive
                user.outsourcingagent.profile_pic=files
                user.outsourcingagent.registerdby = logged_in_user
                user.save()
                messages.success(request,'Agent Add Successfully!!')
            else:
                user = CustomUser.objects.create_user(username=email,first_name=firstname,last_name=lastname,email=email,password=password,user_type='4')

            # users = request.user.username
                logged_in_user = CustomUser.objects.get(username=request.user.username)
            
            
            # print("userssssssssss",users)
                user.agent.type=type
                user.agent.contact_no=contact
                user.agent.country=country
                user.agent.state=state
                user.agent.City=city
                user.agent.Address=address
                user.agent.zipcode=zipcode
                user.agent.activeinactive=activeinactive
                user.agent.profile_pic=files
                user.agent.registerdby = logged_in_user
                user.save()
                messages.success(request,'Agent Add Successfully!!')
        except Exception as e:
            messages.warning(request,e)
    return render(request,'Employee/agentmanagement/addagent.html')
 
class all_agent(ListView):
    model = Agent
    template_name = 'Employee/agentmanagement/agentlist.html'  
    context_object_name = 'agent'

    def get_queryset(self):
        
        return Agent.objects.all().union(OutSourcingAgent.objects.all())
    
def agent_status_update(request):
    
    if request.method == "POST":
        agent_id = request.POST.get('agent_id')
        
        status = request.POST.get('status')
        print("status",status)
        try:
            agent = Agent.objects.get(id=agent_id)
            agent.status = status
            agent.save()
            
        except Agent.DoesNotExist:
            # Handle the case where the agent doesn't exist
            return redirect('Employee_all_agent')  # Redirect to some appropriate URL
        # agent.status = status
        # return redirect('Employee_all_agent')


    return redirect('Employee_all_agent')


class DepartmentCreateView(CreateView):

    model = Department
    form_class = DepartmentForm
    template_name = 'Employee/Rolesmanagement/addrole.html'
    success_url = reverse_lazy('Employee_Department_list') 
    
    
class DepartmentListView(ListView):
    model = Department
    template_name = 'Employee/Rolesmanagement/rolelist.html'  
    context_object_name = 'role'
    
class editDepartment(LoginRequiredMixin,UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'Employee/Rolesmanagement/roleupdate.html'
    success_url = reverse_lazy('Employee_Department_list')

    def form_valid(self, form):
        # Set the lastupdated_by field to the current user's username
        form.instance.lastupdated_by = self.request.user

        # Display a success message
        messages.success(self.request, 'Department Updated Successfully.')

        return super().form_valid(form)
     

@login_required(login_url='/') 
def ChangePassword(request):
    user = request.user
    admin = Admin.objects.get(users=user)
    
    if request.method == "POST":
        old_psw = request.POST.get('old_password')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        
        if check_password(old_psw, admin.users.password):
            if newpassword == confirmpassword:
                # Set the new password for the user
                admin.users.set_password(newpassword)
                admin.users.save()
                messages.success(request,"Password changed successfully Please Login Again !!")
                return HttpResponseRedirect(reverse("ChangePassword"))
            else:
                messages.success(request,"New passwords do not match")
                return HttpResponseRedirect(reverse("ChangePassword"))
                
        else:
            # print("Old password is not correct")
            messages.warning(request,'Old password is not correct')
            
       
    return render(request, 'Employee/ChangePassword/changepassword.html')


class all_appointment(ListView):
    model = Appointment
    template_name = 'Employee/Appointment/appointmentlist.html'
    context_object_name = 'appointment'


def AssignRoleView(request):
    if request.method == "POST":
        department_id = request.POST.get('department')
        menu_choice = request.POST.getlist('menu_choice')
        employee_ids = request.POST.getlist('employee')
        print("Ssssssssssssssss",employee_ids)

        try:
            department = Department.objects.get(id=department_id)
            menu_id = Menu.objects.filter(id__in=menu_choice)
            print("hellooo")
            employees = Employee.objects.filter(id__in=employee_ids)
            
           

            role_assignment = AssignRoles.objects.create(department=department)

            role_assignment.menu_name.set(menu_id)
            
            #Add employees to the role_assignment one by one
            for employee in employees:
                messages.success(request, 'Role assigned successfully.')
                print("emplaaaa",employee)
                role_assignment.employee.add(employee)

            print("success")
            return redirect('Employee_assign_permissions')  # Replace 'success_url' with the appropriate URL

        except Exception as e:
            print("Error:", str(e))
        
        

    # Fetch departments and employees for rendering the form
    departments = Department.objects.all()
    employees = Employee.objects.all()
    menu_choices = Menu.objects.all()

    context = {
        "department": departments,
        "employee": employees,
        "menu_choices": menu_choices,
    }

    return render(request, 'Employee/permission.html', context)

def fetch_users(request):
    
    category_id = request.GET.get('category_id')
    subcategories = Employee.objects.filter(department=category_id)
    # data = list(subcategories.values('id', 'users'))
    data = [{'id': emp.id, 'first_name': emp.users.first_name,'last_name': emp.users.last_name,'department': emp.department.name} for emp in subcategories]
    return JsonResponse(data, safe=False)
    print("category_id",category_id)

def get_users_for_department(request):
    department_id = request.GET.get('department_id')
    if department_id:
        users = CustomUser.objects.filter(employee__department=department_id)
        user_list = [{'id': user.id, 'username': user.username} for user in users]
        return JsonResponse(user_list, safe=False)
    else:
        return JsonResponse([], safe=False)

def handle_permissions(request):
    if request.method == 'POST':
        # Get the selected department, menu choices, and users from the form data
        department_id = request.POST.get('department')
        selected_menu_choices = request.POST.getlist('menu_name')
        selected_users = request.POST.getlist('users')

        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return HttpResponse("Invalid department")

        # Clear existing permissions for the selected department
        AssignRoles.objects.filter(department=department).delete()

        # Assign new permissions based on selected menu choices and users
        for menu_choice in selected_menu_choices:
            # Here, menu_choice will be one of the choices defined in your model
            for user_id in selected_users:
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    return HttpResponse(f"Invalid user ID: {user_id}")

                # Create a new AssignRoles entry for each combination
                AssignRoles.objects.create(department=department, menu_name=menu_choice, users=user)

        return HttpResponse("Permissions assigned successfully")

    # Handle GET requests or other cases
    # You can render a template or return an appropriate response
    return HttpResponse("Invalid request")

def AssignRolelist(request):
    assign_roles = AssignRoles.objects.all()

    context = {
        'assign_roles': assign_roles,
    }

    return render(request, 'Employee/Rolesmanagement/assign_roles_list.html', context)

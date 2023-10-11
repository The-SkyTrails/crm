
from django.urls import path , include
from .AdminViews import *
from .AgentViews import *


urlpatterns = [
    
    # path('Dashboard/', TemplateView.as_view(template_name='Agent/Base/index2.html'), name='agent_dashboard'),
    path('Dashboard',agent_dashboard,name="agent_dashboard"),
    path('Login/', agent_login,name="agent_login"),
    
    path('AddLeads/', AgentEnquiryCreateView.as_view(),name="add_leads"),
    path('AllLeads/', agent_leads,name="agent_leads"),

    path('AppointmentList/',appointment_list.as_view(),name="appointment_list"),
    path('Agent/logout', agent_logout,name="agent_logout"),

]
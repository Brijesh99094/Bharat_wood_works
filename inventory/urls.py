from django.urls import path        
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('users/',views.users,name='users'),
    path('Admin_Dashboard/',views.Admin_dashboard,name='Admin_dashboard'), 
    path('Admin_Dashboard/users', views.users,name='Admin_dashboard_users'),
    path('Dealer_Dashboard/', views.Dealer_dashboard,name='Dealer_Dashboard'),
    path('Customer_Dashboard/', views.Customer_dashboard,name='Customer_Dashboard'),
    path('Supervisor_Dashboard/', views.Supervisor_dashboard,name='Supervisor_Dashboard'),
    path('Company_Dashboard/', views.Company_dashboard,name='Company_Dashboard'),
    path('CustomerDetail/',views.Customer_Detail,name='CustomerDetail'),
    path('DealerDetail/',views.Dealer_Detail,name='DealerDetail'),
    path('SupervisorDetail/',views.Supervisor_Detail,name='SupervisorDetail'),
    path('CompanyDetail/',views.Company_Detail,name='CompanyDetail'),
    path('assignment/<id>',views.assign,name='assignment'),
    path('Update_assignment/<id>',views.Update_assign,name='update_assignment'),
    path('DeleteUser/<id>',views.delete_user,name='DeleteUser'),
    path('delete_assigned_warehouse/<id>',views.delete_assigned_warehouse,name='delete_assigned_warehouse'),
    path('delete_assigned_company/<id>',views.delete_assigned_company,name='delete_assigned_company'),
    path('Profile/<id>/',views.profile,name='userprofile'),
    path('report/',views.report,name='report'),
    
    
]

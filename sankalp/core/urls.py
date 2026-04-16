from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    
    # Student Dash board
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Complaint Management
    path('add-complaint', views.add_complaint, name='add_complaint'),
    path('complaint/<int:pk>', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:pk>/comment', views.add_comment, name='add_comment'),
    path('complaint/<int:pk>/delete', views.delete_complaint, name='delete_complaint'),
    path('complaint/<int:pk>/update-status', views.update_complaint_status, name='update_complaint_status'),
    path('search', views.search_complaints, name='search_complaints'),
    
    # User Profile
    path('profile', views.profile, name='profile'),
    path('profile/update', views.update_profile, name='update_profile'),
    path('profile/change-password', views.change_password, name='change_password'),
    
    # Admin
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin/complaint/<int:pk>', views.admin_edit_complaint, name='admin_edit_complaint'),
]

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/<str:token>', views.reset_password, name='reset_password'),
    path('verify-email/<int:user_id>/<str:token>', views.verify_email, name='verify_email'),
    path('resend-verification', views.resend_verification, name='resend_verification'),

    # Student Dashboard
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

    # Admin  (use admin-panel/ prefix to avoid conflict with Django's built-in /admin/)
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/complaint/<int:pk>', views.admin_edit_complaint, name='admin_edit_complaint'),
    path('admin-panel/assign/<int:pk>', views.assign_complaint, name='assign_complaint'),
    path('admin-panel/users', views.admin_manage_users, name='admin_manage_users'),
    path('admin-panel/reports', views.admin_reports, name='admin_reports'),
    path('admin-panel/activity', views.admin_recent_activity, name='admin_recent_activity'),
    path('admin-panel/export/complaints', views.export_complaints_excel, name='export_complaints_excel'),
    path('admin-panel/export/statistics', views.export_statistics_excel, name='export_statistics_excel'),

    # Terms and Support
    path('terms-and-conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('contact-support', views.contact_support, name='contact_support'),
]

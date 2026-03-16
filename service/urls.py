from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home_page'),
    path('home/', views.homePage, name='home'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),

    path('profile_view/', views.profile_view, name='profile_view'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),

    path('notifications/', views.notifications_view, name='notifications'),

    path('admin_students/', views.admin_students, name="admin_students"),
    path('admin_drivers/', views.admin_drivers, name="admin_drivers"),
    path('admin_buses/', views.admin_buses, name="admin_buses"),
    path('admin_routes/', views.admin_routes, name="admin_routes"),
    path('admin_attendance/', views.admin_attendance, name="admin_attendance"),
    path('admin_complaints/', views.admin_complaints, name="admin_complaints"),
    path('admin_announcements/', views.admin_announcement, name="admin_announcements"),
path('admin/students/add/', views.add_student, name="add_student"),
path('admin/students/edit/<int:id>/', views.edit_student, name="edit_student"),
path('admin/students/delete/<int:id>/', views.delete_student, name="delete_student"),

    path('hi/', views.hi, name='hi'),
]
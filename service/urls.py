from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('hi/', views.hi, name='hi'),
    path('home/', views.homePage, name='home'),
    path('', views.homePage, name='home_page'),
    path('student-dashboard/',views.student_dashboard, name='student_dashboard'),
    path('profile_view/',views.profile_view, name='profile_view'),
    path('profile_edit/',views.profile_edit, name='profile_edit'),
    path('logout/',views.logout_view,name='logout'),
    path('notifications/',views.notifications_view,name='notifications'),
    path('driver-dashboard/',views.driver_dashboard,name='driver_dashboard'),
    path("manager-dashboard/", views.manager_dashboard, name="manager_dashboard"),
]
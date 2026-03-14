from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from service.models import AccountProfile, Student, Driver,Bus,Route,Announcement
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
import re

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not user.is_active:
                return HttpResponseBadRequest("Account is inactive")

            login(request, user)

            profile = AccountProfile.objects.filter(user=user).first()
            role = profile.role

            if role == "admin":
                return redirect("admin_dashboard")

            elif role == "student":
                return render(request,'student_dashboard.html')

            elif role == "driver":
                return redirect("driver_dashboard")

        else:
            return HttpResponseBadRequest("Invalid username or password")

    return render(request, "login.html")

def homePage(request):
    return render(request,'homePage.html')
def admin_dashboard(request):
    return HttpResponse("Admin Dashboard")

def student_dashboard(request):

    student = Student.objects.get(user=request.user)

    route = student.route

    announcements = Announcement.objects.all()

    context = {
        "student": student,
        "route": route,
        "announcements": announcements
    }

    return render(request, "student_dashboard.html", context)
def driver_dashboard(request):
    return HttpResponse("Driver Dashboard")


def signup_view(request):
    from django.conf import settings
    print("DB PATH:", settings.DATABASES['default']['NAME'])

    routes = Route.objects.all()
    print("ROUTES:", routes)
    
    routes = Route.objects.all()
    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        reg_number = request.POST.get("reg_number")
        department = request.POST.get("department")
        semester = request.POST.get("semester")
        route_id = request.POST.get("route")
        card_id = request.POST.get("transport_card_id")

        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        # Email validation
        pattern = r'^(sp|fa)(23|24|25|26)-(bse|cs|me|cve|ee|ms)-[0-9]{3}@students\.comsats\.edu\.pk$'
        pattern2 = r'^(SP|FA)(23|24|25|26)-(BSE|CS|ME|CVE|EE|MS)-[0-9]{3}$'
        if not re.match(pattern, email):
            messages.error(request, "Please enter a valid COMSATS email")
            return redirect("signup")
        if not re.match(pattern2, reg_number):
            messages.error(request, "Registration number must be in format SP23-BSE-001")
            return redirect("signup")

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_active=False  # Admin approval required
        )

        # Create Account Profile
        AccountProfile.objects.create(
            user=user,
            role="student",
            phone_number=phone
        )

        # Get route
        route = None
        if route_id:
            route = Route.objects.get(id=route_id)

        Student.objects.create(
            user=user,
            reg_number=reg_number,
            department=department,
            semester=semester,
            route=route,
            transport_card_id=card_id,
            fee_status="pending"
        )
        messages.success(request, "Account created. Wait for admin approval.")

        return redirect("login")

    return render(request, "signup.html", {
        "routes": routes
    })

def hi(request):
    routes = Route.objects.all()
    return HttpResponse(routes)
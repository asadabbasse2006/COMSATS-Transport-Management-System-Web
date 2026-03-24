from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
import re
from datetime import date
from django.core.mail import send_mail
from job_portal import settings
from service.models import Route, AccountProfile, Student,Announcement,Bus,Driver,Attendance,Driver
from service.forms import ProfileEditForm

import random

def generate_otp():
    return str(random.randint(100000,999999))

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            profile = AccountProfile.objects.get(user=user)

            otp = generate_otp()
            profile.otp = otp
            profile.save()
            print(otp)
            send_mail(
                "Password Reset OTP",
                f"Your OTP is: {otp}",
                "asadse2006@gmail.com",
                [email],
                fail_silently=False
            )

            request.session['reset_email'] = email
            return redirect('verify_otp')

        except:
            return render(request,'forgot_password.html',{'error':'Email not found'})

    return render(request,'forgot_password.html')

def verify_otp(request):

    if request.method == "POST":
        otp = request.POST.get('otp')
        email = request.session.get('reset_email')

        user = User.objects.get(email=email)
        profile = AccountProfile.objects.get(user=user)

        if profile.otp == otp:
            return redirect('new_password')

        else:
            return render(request,'verify_otp.html',{'error':'Invalid OTP'})

    return render(request,'verify_otp.html')

def new_password(request):

    if request.method == "POST":
        password = request.POST.get('password')
        email = request.session.get('reset_email')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        return redirect('login')

    return render(request,'new_password.html')


def email(receiver):
    send_mail(
        'Login Alert',
        'You have logged in successfully',
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False,

    )

def signUpEmail(receiver):
    send_mail(
        'Signup Alert',
        'Your account has been created successfully.\n\nWait for admin approval.',
        settings.EMAIL_HOST_USER,
        [receiver],
        fail_silently=False
    )
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if not user.is_active:
                return HttpResponseBadRequest("Account is inactive")

            profile = AccountProfile.objects.filter(user=user).first()
            email_receiver = user.email
            email(email_receiver)
            if profile is None:
                return HttpResponseBadRequest("User profile not found")

            login(request, user)

            role = request.POST.get('role')

            if role == "admin":
                return redirect("admin_dashboard")

            elif role == "student":
                return redirect("student_dashboard")

            elif role == "driver":
                return redirect("driver_dashboard")

            else:
                return HttpResponseBadRequest("Invalid role")

        else:
            return HttpResponseBadRequest("Invalid username or password")

    return render(request, "login.html")

@login_required
def manager_dashboard(request):

    routes_count = Route.objects.count()
    buses_count = Bus.objects.count()
    drivers_count = Driver.objects.count()
    students_count = Student.objects.count()

    complaints = Complaint.objects.all().order_by("-complaint_date")[:5]

    announcements = Announcement.objects.all().order_by("-date")[:5]

    context = {
        "routes_count": routes_count,
        "buses_count": buses_count,
        "drivers_count": drivers_count,
        "students_count": students_count,
        "complaints": complaints,
        "announcements": announcements
    }

    return render(request,"manager_dashboard.html",context)
@login_required
def driver_dashboard(request):

    driver = Driver.objects.filter(user=request.user).first()

    if not driver:
        return HttpResponse("Driver profile not found")

    bus = driver.assigned_bus
    route = bus.route

    students = Student.objects.filter(route=route)

    announcements = Announcement.objects.all()

    profile = AccountProfile.objects.get(user=request.user)
    phone = profile.phone_number if profile else None

    if request.method == "POST":

        present_students = request.POST.getlist("attendance")

        for student in students:

            present = str(student.id) in present_students

            Attendance.objects.update_or_create(
                student=student,
                attendance_date=date.today(),
                defaults={
                    "bus": bus,
                    "is_present": present
                }
            )

        return redirect("driver_dashboard")

    today_attendance = Attendance.objects.filter(
        bus=bus,
        attendance_date=date.today(),
        is_present=True
    )

    present_today = today_attendance.count()

    context = {
        "driver": driver,
        "bus": bus,
        "route": route,
        "students": students,
        "announcements": announcements,
        "present_today": present_today,
        "phone": phone
    }

    return render(request, "driver_dashboard.html", context)
def admin_dashboard(request):

    students = Student.objects.all()
    drivers = Driver.objects.all()
    buses = Bus.objects.all()
    routes = Route.objects.all()
    complaints = Complaint.objects.all().order_by('id')[:5]
    context = {
        "students":students,
        "drivers":drivers,
        "buses":buses,
        "routes":routes,
        "complaints":complaints
    }

    return render(request,"admin_dashboard.html",context)

def admin_students(request):
    students = Student.objects.all().order_by('reg_number')

    # Get filter values
    search_query = request.GET.get('search')
    batch = request.GET.get('batch')
    route_id = request.GET.get('route')

    # 🔍 Search (name + reg number)
    if search_query:
        students = students.filter(
            reg_number__icontains=search_query
        ) | students.filter(
            user__first_name__icontains=search_query
        ) | students.filter(
            user__last_name__icontains=search_query
        )

    # 🎓 Batch filter (SP23, FA24 etc.)
    if batch:
        students = students.filter(reg_number__icontains=batch)

    # 🚌 Route filter
    if route_id:
        students = students.filter(route__id=route_id)

    # For dropdown
    routes = Route.objects.all()

    # 🔥 Dynamic batch list
    reg_numbers = Student.objects.values_list('reg_number', flat=True)
    batch_list = sorted(set([reg[:4] for reg in reg_numbers if reg]))

    context = {
        "students": students,
        "routes": routes,
        "batch_list": batch_list,
    }

    return render(request, "admin_students.html", context)


def admin_drivers(request):
    drivers = Driver.objects.all()
    return render(request, "admin_drivers.html", {"drivers": drivers})


def admin_buses(request):
    buses = Bus.objects.all()
    return render(request, "admin_buses.html", {"buses": buses})

def edit_bus(request, id):

    bus = Bus.objects.get(id=id)
    routes = Route.objects.all()

    if request.method == "POST":

        bus.bus_number = request.POST.get("bus_no")
        bus.capacity = request.POST.get("capacity")
        bus.route = Route.objects.get(id=request.POST.get("route"))
        bus.is_active = True if request.POST.get("is_active") == "on" else False

        bus.save()

        return redirect('admin_buses')

    return render(request, "edit_bus.html", {
        "bus": bus,
        "routes": routes
    })
def add_announcement(request):

    if request.method == "POST":

        title = request.POST.get("title")
        message = request.POST.get("message")
        audience = request.POST.get("audience")
        expiry = request.POST.get("expiry_date")

        announcement = Announcement.objects.create(
            title=title,
            message=message,
            audience=audience,
            expiry_date=expiry if expiry else None
        )

        # 🔥 Send email automatically
        send_announcement_email(title, message)

        return redirect('admin_announcements')

    return render(request, "add_announcement.html")

def edit_announcement(request, id):

    announcement = Announcement.objects.get(id=id)

    if request.method == "POST":

        announcement.title = request.POST.get("title")
        announcement.message = request.POST.get("message")
        announcement.audience = request.POST.get("audience")
        announcement.expiry_date = request.POST.get("expiry_date") or None
        announcement.is_active = True if request.POST.get("is_active") == "on" else False

        announcement.save()

        return redirect('admin_announcements')

    return render(request, "edit_announcement.html", {
        "announcement": announcement
    })

def update_complaint_status(request, id, status):
    complaint = Complaint.objects.get(id=id)
    complaint.status = status
    complaint.save()
    return redirect('admin_complaints')

from django.shortcuts import get_object_or_404

def delete_announcement(request, id):

    announcement = get_object_or_404(Announcement, id=id)

    announcement.delete()

    return redirect('admin_announcement')

from django.core.mail import send_mail
from django.contrib.auth.models import User

def send_announcement_email(title, message):

    users = User.objects.exclude(email="")

    emails = [user.email for user in users]

    send_mail(
        subject=title,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=True
    )

def delete_bus(request,id):
    bus = Bus.objects.get(id=id)
    bus.delete()
    return redirect('admin_buses')

def admin_routes(request):
    routes = Route.objects.all()
    return render(request, "admin_routes.html", {"routes": routes})


def admin_attendance(request):
    attendance = Attendance.objects.all()
    return render(request, "admin_attendance.html", {"attendance": attendance})


def admin_complaints(request):
    complaints = Complaint.objects.all()
    complaints = Complaint.objects.all()
    return render(request, "admin_complaints.html", {"complaints": complaints})


def admin_announcement(request):
    announcements = Announcement.objects.all()
    return render(request, "admin_announcements.html", {"announcements": announcements})

def edit_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == "POST":

        student.reg_number = request.POST.get("reg")

        # Update name (stored in User model)
        student.user.first_name = request.POST.get("name")
        student.user.save()

        # Update route
        route = request.POST.get("route")
        student.route = Route.objects.get(id=route)

        # Update fee status
        student.fee_status = request.POST.get("fee_status")

        student.save()

        return redirect("admin_students")

    routes = Route.objects.all()

    context = {
        "student": student,
        "routes": routes
    }

    return render(request, "edit_student.html", context)

def add_student(request):

    routes = Route.objects.all()

    if request.method == "POST":

        reg = request.POST.get("reg")
        route_id = request.POST.get("route")

        route = Route.objects.get(id=route_id)

        # create user automatically
        user = User.objects.create_user(
            username=reg,
            password="123456"
        )

        Student.objects.create(
            user=user,
            reg_number=reg,
            department="Unknown",
            semester=1,
            route=route,
            transport_card_id=reg,
            fee_status="Unpaid"
        )

        return redirect('admin_students')

    return render(request, "add_student.html", {"routes": routes})

def add_driver(request):
    buses = Bus.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        assigned_bus_id = request.POST.get("assigned_bus")
        license_number = request.POST.get("license_number")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('add_driver')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        bus_obj = Bus.objects.get(id=assigned_bus_id)

        Driver.objects.create(
            user=user,
            assigned_bus=bus_obj,
            license_number=license_number
        )

        messages.success(request, "Driver added successfully!")
        return redirect('admin_drivers')

    return render(request, "add_driver.html", {"bus": buses})

def edit_driver(request, id):
    driver = Driver.objects.get(id=id)
    buses = Bus.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        bus_id = request.POST.get("assigned_bus")
        license_number = request.POST.get("license_number")

        # Update user info
        driver.user.username = username
        if password:  # only update if provided
            driver.user.set_password(password)
        driver.user.save()

        # Update driver info
        driver.assigned_bus = Bus.objects.get(id=bus_id)
        driver.license_number = license_number

        driver.save()
        messages.success(request, "You have successfully edited the driver")

        return redirect('admin_drivers')

    return render(request, "edit_driver.html", {
        "driver": driver,
        "buses": buses
    })


def delete_driver(request, id):

    driver = get_object_or_404(Driver, id=id)

    driver.delete()

    return redirect('admin_drivers')


def add_bus(request):

    routes = Route.objects.all()

    if request.method == "POST":

        bus_no = request.POST.get("bus_no")
        capacity = request.POST.get("capacity")
        route_id = request.POST.get("route")

        # checkbox handling
        is_active = True if request.POST.get("is_active") == "on" else False

        route = Route.objects.get(id=route_id)

        Bus.objects.create(
            bus_number=bus_no,
            capacity=capacity,
            route=route,
            is_active=is_active
        )

        return redirect('admin_buses')
    return render(request, "add_bus.html", {"routes": routes})

def delete_student(request, id):

    student = Student.objects.get(id=id)
    student.delete()

    return redirect("admin_students")

from .models import Complaint
def student_dashboard(request):
    profile = AccountProfile.objects.get(user=request.user)

    if profile.role != "student":
        return HttpResponseBadRequest("Access denied")

    student = Student.objects.get(user=request.user)
    route = student.route
    announcements = Announcement.objects.all()

    # Safe bus fetch
    bus = Bus.objects.filter(route=route).first()

    # ✅ Correct attendance
    attendance = Attendance.objects.filter(student=student)

    total_rides = attendance.count()
    present_rides = attendance.filter(is_present=True).count()
    absent_rides = total_rides - present_rides

    per = (present_rides / total_rides * 100) if total_rides > 0 else 0

    # Driver
    driver = Driver.objects.filter(assigned_bus=bus).first()
    driver_name = driver.user.get_full_name() if driver else "Not Assigned"

    # Complaint system
    if request.method == "POST":
        message = request.POST.get("message")
        complaint_type = request.POST.get("complaint_type")

        if message:
            full_message = f"{complaint_type}: {message}" if complaint_type else message

            Complaint.objects.create(
                student=student,
                message=full_message,
                status="pending"
            )

            return redirect("student_dashboard")

    # ✅ Fixed ordering
    complaints = Complaint.objects.filter(student=student).order_by("-id")

    context = {
        "student": student,
        "route": route,
        "announcements": announcements,
        "bus": bus,
        "driver_name": driver_name,
        "complaints": complaints,
        "total_rides": total_rides,
        "present_rides": present_rides,
        "absent_rides": absent_rides,
        "per": round(per, 2),
        "attendance": attendance
    }

    return render(request, "student_dashboard.html", context)
@login_required
def profile_view(request):
    user = request.user
    return render(request,'profile_view.html',{"user":user})

def logout_view(request):
    logout(request)
    return redirect('login')

def notifications_view(request):
    announcements = Announcement.objects.all().order_by('-date')

    return render(request, "notifications.html", {
        "announcements": announcements
    })
@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'profile_edit.html', {'form': form})
def homePage(request):
    routes = Route.objects.all()
    return render(request, "homePage.html",{"routes": routes})


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
        pattern_email = r'^(sp|fa)2[3-6]-(bse|cs|me|cve|ee|ms)-[0-9]{3}@students\.cuisahiwal\.edu\.pk$'
        pattern_reg = r'^(SP|FA)2[3-6]-(BSE|CS|ME|CVE|EE|MS)-[0-9]{3}$'
        if not re.match(pattern_email, email):
            messages.error(request, "Please enter a valid COMSATS email")
            return redirect("signup")
        if not re.match(pattern_reg, reg_number):
            messages.error(request, "Registration number must be in format SP23-BSE-001")
            return redirect("signup")

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_active=False  # Admin approval required
        )

        signUpEmail(email)

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
from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Route Model
# -----------------------------
class Route(models.Model):
    route_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.route_name} ({self.start_location} → {self.end_location})"


# -----------------------------
# Bus Model
# -----------------------------
class Bus(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    bus_number = models.CharField(max_length=20)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Bus {self.bus_number} - Route {self.route.route_name}"


# -----------------------------
# Account Profile (Role System)
# -----------------------------
class AccountProfile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('driver', 'Driver'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    semester = models.IntegerField(default=False)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    transport_card_id = models.CharField(max_length=20, unique=True)
    fee_status = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.reg_number})"


# -----------------------------
# Driver Model
# -----------------------------
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, unique=True)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"


# -----------------------------
# Seat Allocation
# -----------------------------
class SeatAllocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    allocation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('bus', 'seat_number')

    def __str__(self):
        return f"{self.student} - Bus {self.bus.bus_number} Seat {self.seat_number}"


# -----------------------------
# Payment
# -----------------------------
class Payment(models.Model):

    PAYMENT_STATUS = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"{self.student} - {self.amount} ({self.payment_status})"


# -----------------------------
# Complaint
# -----------------------------
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

# -----------------------------
# Attendance
# -----------------------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    attendance_date = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.attendance_date}"


class Announcement(models.Model):

    title = models.CharField(max_length=200)
    message = models.TextField()

    # Target audience
    audience = models.CharField(
        max_length=20,
        choices=[
            ('all', 'All'),
            ('student', 'Students'),
            ('driver', 'Drivers')
        ],
        default='all'
    )

    # Active system
    is_active = models.BooleanField(default=True)

    # Expiry date
    expiry_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
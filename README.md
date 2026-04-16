# 🚍 Transport Management System (TMS) – COMSATS Sahiwal

### Smart Digital Solution for Student Transport & Fleet Management

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat\&logo=python\&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat\&logo=django\&logoColor=white)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Project Overview

The **Transport Management System (TMS)** is a full-stack web application developed for **COMSATS University Islamabad, Sahiwal Campus**.

It digitizes and automates the entire transport process including:

* Student registration
* Route and bus management
* Attendance tracking
* Complaint handling
* QR-based transport cards

This system replaces traditional manual processes with a **secure, scalable, and efficient digital solution**.

---

## 🚀 Key Features

### 🔐 Authentication & Roles

* Role-based login system (Admin, Student, Driver)
* Secure authentication using Django Auth system
* Profile-based access control

### 👨‍🎓 Student Management

* Add, update, delete student records
* Unique registration & transport card IDs
* Fee status tracking (Paid / Unpaid)

### 🚌 Transport & Routing

* Bus assignment to routes
* Route scheduling (departure & arrival)
* Driver allocation system

### 📊 Attendance System

* Track daily attendance per student
* Calculate:

  * Total rides
  * Present rides
  * Attendance percentage
* Visual dashboard with progress bar

### 📢 Announcement System

* Admin can post announcements
* Audience targeting (All / Students / Drivers)
* Expiry-based filtering

### 📩 Complaint Management

* Students can submit complaints
* Complaint categories:

  * Bus Delay
  * Driver Behavior
  * Cleanliness
* Track complaint status (Pending / Resolved)

### 🧾 QR Code Transport Card

* Auto-generated QR codes for each student
* Unique transport card system
* Ready for future scanning integration

### 📈 Dashboard Analytics

* Student dashboard with:

  * Route info
  * Driver details
  * Attendance stats
  * Complaint history

---

## 🧠 Upcoming Features (In Progress 🚧)

* 🔌 REST API using Django REST Framework
* 📱 Flutter Mobile App Integration
* 📊 Chart.js Analytics Dashboard
* 🔐 JWT Authentication
* 📡 Real-time Notifications

---

## 🛠 Tech Stack

| Layer        | Technology                           |
| ------------ | ------------------------------------ |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Backend**  | Django (Python)                      |
| **Database** | SQLite (Development) / MySQL         |
| **Others**   | QRCode, Django Messages Framework    |

---

## 📁 Project Structure

```text
job_portal/
│
├── job_portal/         # Project configuration
├── service/            # Main application
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   ├── urls.py         # Routing
│   ├── templates/      # HTML templates
│   └── migrations/     # DB migrations
│
├── static/             # CSS, JS, images
├── templates/          # Global templates
├── db.sqlite3          # Database
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/asadabbasse2006/transport-management-system.git
cd transport-management-system
```

### 2️⃣ Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🌐 Usage

* Main App → http://127.0.0.1:8000/
* Admin Panel → http://127.0.0.1:8000/admin/

---

## 🧪 Testing Credentials (Optional)

> Add demo credentials here if needed for reviewers

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to GitHub
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Asad Abbas**
🎓 BS Software Engineering – COMSATS Sahiwal
📧 [asadse2006@gmail.com](mailto:asadse2006@gmail.com)
🔗 GitHub: https://github.com/asadabbasse2006

---

## ⭐ Final Note

This project demonstrates:

* Full-stack Django development
* Database design & relationships
* Real-world system architecture
* Problem-solving for university logistics

🚀 Future goal: Convert this system into a **REST API + Mobile Application (Flutter)**.

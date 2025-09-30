# 🩸 Blood Donation Management Platform

A **Flask-based web application** to connect **donors, hospitals, organizations, and admins** for managing blood donation activities with secure role-based access.

---

## 📖 Table of Contents

* [Features](#-features)
* [Quick Setup](#-quick-setup)
* [Project Structure](#-project-structure)
* [User Roles](#-user-roles)
* [Development Details](#-development-details)
* [API Endpoints](#-api-endpoints)
* [Production Deployment](#-production-deployment)
* [License](#-license)

---

## 🚀 Features

<details>
<summary>Click to expand</summary>

* 🔑 **Role-Based System**

  * Donors: Register, manage profiles, track donation history
  * Hospitals: Request blood, manage urgent needs
  * Organizations: Organize events, manage donor networks
  * Admins: Manage users and platform settings

* 🩸 **Core Functionality**

  * Secure login & authentication
  * Blood type compatibility matching
  * Search/filter donors
  * Emergency request system
  * Real-time notifications & alerts

* 📱 **Responsive Design** – Works on mobile and desktop

* 🔐 **Security Features** – CSRF protection, password hashing, role-based access control

</details>

---

## 🛠️ Quick Setup

<details>
<summary>Click to expand</summary>

### 1. Prerequisites

* Python 3.11+
* PostgreSQL (production) or SQLite (development)

### 2. Installation

```bash
unzip blood_donation_platform_source.zip
cd blood_donation_platform

pip install -r requirements.txt
# or
uv sync
```

### 3. Set Environment Variables

```bash
export SESSION_SECRET="your-secret-key"
export DATABASE_URL="sqlite:///instance/blood_donation.db"
```

### 4. Run the Application

```bash
# Development
python main.py

# Production
gunicorn --bind 0.0.0.0:5000 main:app
```

Open: [http://localhost:5000](http://localhost:5000)

</details>

---

## 📂 Project Structure

<details>
<summary>Click to expand</summary>

```
blood_donation_platform/
├── app.py              # Flask app setup
├── models.py           # Database models
├── routes.py           # Routes & controllers
├── forms.py            # WTForms definitions
├── utils.py            # Helper functions
├── main.py             # Entry point
├── static/
│   ├── css/            # Custom CSS
│   └── js/             # JavaScript
└── templates/          # Jinja2 templates
    ├── auth/           # Login/Register
    ├── donor/          # Donor dashboard
    ├── hospital/       # Hospital dashboard
    ├── organization/   # Organization dashboard
    ├── admin/          # Admin panel
    └── search/         # Search functionality
```

</details>

---

## 👥 User Roles

<details>
<summary>Click to expand</summary>

* **Donor**

  * Complete profile with medical info
  * Check donation eligibility
  * Respond to hospital requests
  * Track history

* **Hospital**

  * Create urgent requests
  * Manage hospital profile
  * View donor responses

* **Organization**

  * Organize donation events
  * Manage donor network
  * Collaborate with hospitals

* **Admin**

  * User & role management
  * System oversight
  * Analytics and reporting

</details>

---

## 🧑‍💻 Development Details

<details>
<summary>Click to expand</summary>

### Technologies Used

* **Backend:** Python, Flask, SQLAlchemy, WTForms
* **Frontend:** HTML, CSS, JavaScript
* **Database:** PostgreSQL (prod), SQLite (dev)
* **Server:** Gunicorn (prod)

### Database Models

* `User` – Base user authentication
* `DonorProfile` – Donor info
* `HospitalProfile` – Hospital details
* `OrganizationProfile` – Organization info
* `BloodRequest` – Requests made by hospitals
* `Donation` – Records of donations
* `DonationEvent` – Organized events

</details>

---

## 🔗 API Endpoints

<details>
<summary>Click to expand</summary>

* **Authentication:** `/login`, `/register`, `/logout`
* **Dashboards:** `/dashboard`, `/donor/dashboard`, `/hospital/dashboard`
* **Profiles:** `/donor/profile`, `/hospital/profile`, `/organization/profile`
* **Search:** `/search/donors`
* **Requests:** `/hospital/request-blood`

</details>

---

## ☁️ Production Deployment

<details>
<summary>Click to expand</summary>

* Use **PostgreSQL** with secure credentials
* Configure **Gunicorn** as WSGI server
* Enable **HTTPS** with SSL
* Add **security headers**
* Set up monitoring/logging

</details>

---

## 📜 License

MIT License

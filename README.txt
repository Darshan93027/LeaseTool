===============================
🔧 LeaseTool - Setup Guide
===============================

LeaseTool is a Django-based Tool Rental & Lease Management System. It supports OTP-based email verification, tool tracking, overdue calculations, and a REST API layer.

This guide will help you:
✔ Setup virtual environment
✔ Configure .env file
✔ Set up database & email
✔ Run Django project
✔ Use API with Postman

--------------------------------
📁 Project Folder Structure
--------------------------------

LeaseTool/
│
├── venv/                     ← virtual environment folder (excluded from Git)
├── LeaseTool                 ← Main Django app
├── manage.py
├── requirements.txt
├── .env.example              ← Sample env config
├── api_collection.json       ← Postman API collection
├── postman_environment.json  ← Postman environment config
├── README.txt                ← This file

============================
🧰 1. Requirements
============================

- Python 3.8 or newer
- pip
- MySQL running on port 3300
- Git
- Postman (for API testing)

============================
🐍 2. Virtual Environment Setup
============================

If not already present, create virtual environment:

For Windows:
    python -m venv venv
    venv\Scripts\activate

For macOS/Linux:
    python3 -m venv venv
    source venv/bin/activate

Install dependencies:
    pip install -r requirements.txt

============================
🔐 3. Create and Configure .env
============================

Create your `.env` file:

On macOS/Linux:
    cp .env.example .env

Or manually create `.env` and paste:

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD='your_app_password'

# Database settings
DB_ENGINE=django.db.backends.mysql
DB_NAME=LeaseTool
DB_USER=your_user_name
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3300


============================
🧪 4. Django Setup Commands
============================

Activate virtual env, then run:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Open in browser:
    http://127.0.0.1:8000/

============================
📬 5. Postman API Collection
============================

To test APIs via Postman:

1. Import "api_collection.json" into Postman as Collection.
2. Import "postman_environment.json" into Postman as Environment.
3. Select the environment and run requests like:
   - Tool Create / Update
   - Lessee Register
   - Return Tool
   - Check Tool Availability



============================
📦 6. Common Django Commands
============================

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    python manage.py createsuperuser
   




Darshan Sharma  
Email: contactdarshan07@gmail.com

============================
🎉 All Set!
============================


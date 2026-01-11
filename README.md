## 📦 Project Setup Steps


cd task_manager 

cd config 

2️⃣ Create Virtual Environment

python -m venv venv

venv\Scripts\activate

3️⃣ Install Dependencies

pip install -r requirements.txt

🗄️ Migration Steps

4️⃣ Create Migrations

python manage.py makemigrations

5️⃣ Apply Migrations

python manage.py migrate

6️⃣ Create Superuser

python manage.py createsuperuser

7️⃣ Run Django Server

python manage.py runserver


Admin panel:
http://127.0.0.1:8000/admin/


🔄 Celery & Redis Setup

2,NEW Terminal

8️⃣ Start Redis

cd task_manager

cd config 

redis-server

3,NEW Terminal

9️⃣ Start Celery Worker (Windows)

cd task_manager

cd config 

celery -A config worker -l info --pool=solo

4,NEW Terminal

🔟 Start Celery Beat (Scheduler)

cd task_manager

cd config 

celery -A config beat -l info


Celery Beat runs scheduled jobs (overdue task checker)

📧 Email Configuration

Emails are sent automatically when a task becomes OVERDUE.

Configure in settings.py:

EMAIL_HOST_USER = 'your_email@gmail.com'

EMAIL_HOST_PASSWORD = 'your_app_password'


⚠️ Use Gmail App Password, not your normal password.

🔌 API Documentation

🔐 Authentication

Method	Endpoint	Description

POST	/api/auth/login/	JWT Login

POST	/api/auth/refresh/	Refresh Token

📝 Tasks API

Method	Endpoint	Access

GET	/api/tasks/	All authenticated users

POST	/api/tasks/	ADMIN

GET	/api/tasks/{id}/	Owner / Assigned

PUT	/api/tasks/{id}/	Owner / Assigned

DELETE	/api/tasks/{id}/	ADMIN only

🧪 Background Job

Automatic Overdue Task Job

Runs every minute (configurable)

Finds overdue tasks

Updates status

Logs activity

Sends email alerts

Task location:

tasks/tasks.py → mark_overdue_tasks


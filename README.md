
# 📄 Stage 1: Backend Setup Document
## Project: Ecommerce Platform (Django + MySQL)

---

## ✅ Objectives
- Setup Django backend project
- Connect with MySQL database
- Prepare media upload handling for product images
- Ready for user authentication and product APIs
- Deployment-ready folder structure

---

## 📁 Folder Structure

```
ecommerce-project/
├── backend/
│   ├── api/                    # App for all business logic
│   ├── backend/                # Django settings and main project
│   ├── media/                  # Folder for uploaded product images
│   ├── manage.py
│   └── requirements.txt
├── venv/                       # Python virtual environment
```

---

## 🧱 Step-by-Step Setup

### 1️⃣ Create Folder and Virtual Environment

```bash
mkdir ecommerce-project
cd ecommerce-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

---

### 2️⃣ Install Required Packages

```bash
pip install django djangorestframework mysqlclient python-decouple django-cors-headers
pip freeze > requirements.txt
```

#### 📄 `requirements.txt`

```txt
Django>=4.0
djangorestframework>=3.13
mysqlclient>=2.1
python-decouple>=3.6
django-cors-headers>=3.13
```

---

### 3️⃣ Create Django Project and App

```bash
django-admin startproject backend .
cd backend
python manage.py startapp api
```

---

### 4️⃣ Update `settings.py`

#### Add Apps

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'api',
]
```

#### Add Middleware

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
```

#### CORS Configuration

```python
CORS_ALLOW_ALL_ORIGINS = True
```

#### Media Configuration

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

#### MySQL Database Settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

### 5️⃣ Setup URLs (`backend/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # create this file later
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### 6️⃣ Final Setup Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## ✅ Outcome of Stage 1

- ✅ Django project and API app are created
- ✅ MySQL database is connected and functional
- ✅ Media file upload support is in place
- ✅ CORS is enabled for frontend communication
- ✅ Ready to create user authentication and product APIs

---

## 🛠 Git Setup

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg
*.egg-info/
*.pyo
*.pyd
*.pyc
.Python
.env
venv/
*.sqlite3

# Django
db.sqlite3
media/
staticfiles/
*.log

# VS Code
.vscode/

# MacOS
.DS_Store

# Env/Secrets
.env
.env.*

# Migrations (optional, keep if you want control)
**/migrations/*.py
!**/migrations/__init__.py
```


## Project: Ecommerce Platform (Django + MySQL)
# 📄 Stage 1: Backend Setup Document
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
#cd backend
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



---

## ✅ Outcome of Stage 1

-  Just test your available URLs
-  Visit:
    http://127.0.0.1:8000/admin/ → Django admin panel

    http://127.0.0.1:8000/api/ → This will show something only if you define routes in api/urls.py

- If you're just testing, it's totally fine to leave the root (/) path undefined.

---


## ✅ Add a welcome route (optional)
- If you want to show a simple message at /, add this to your backend/urls.py:

```bash
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Ecommerce API")

urlpatterns = [
    path('', home),  # 👈 Add this line
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```



# Stage 2: User Authentication with JWT (Updated)

In this stage, we'll set up **JWT Authentication** for user registration, login, and retrieving user information. The user model will only have a boolean field `is_admin`, which is used to differentiate between an admin and a common user. Additionally, email uniqueness is enforced during registration.

---
## 📁 Now Folder Structure

```
├── backend/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
├── api/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ └── migrations/
├── media/
├── manage.py
├── requirements.txt
└── .gitignore

```

---
## 1. Custom User Model

We will use a custom user model in Django to manage users. This custom model extends Django’s `AbstractUser`, and includes the `is_admin` field and ensures that the `email` field is unique.

### **`models.py`**

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    is_admin = models.BooleanField(default=False)  # Admin or common user

    def __str__(self):
        return self.username
```

### Explanation:
- **`CustomUser`** extends Django’s built-in `AbstractUser`, so we keep all the default user features.
- **`is_admin`** field determines whether the user is an admin (True) or a common user (False).
- **`email`** is set as unique to prevent multiple users from registering with the same email address.

---

## 2. Register Serializer

The `RegisterSerializer` ensures user data is properly validated and created in the database. We also added email validation to check if the email already exists.

### **`serializers.py`**

```python
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_admin']
        extra_kwargs = {
            'password':{'write_only':True},
            'email':{'required':True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data['email']
        # email = validated_data.get('email')
        username = email
        validated_data['username'] = email           # Set username = email

            # explicitly create user with username=email
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_admin=validated_data.get('is_admin', False)
        )
        user.save()
        return user
    
User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']
```

### Explanation:
- **`validate_email`** checks if the email already exists in the database. If it does, a validation error is raised.
- **`create_user`** ensures that the user’s password is securely hashed before saving to the database.

---

## 3. Login Serializer and View

The `LoginView` will authenticate users and generate **JWT tokens** (access and refresh tokens) for them. 

### **`views.py`**

```python
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg':'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access':str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error':'Invalid creadentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

```

### Explanation:
- **`RegisterView`** handles user registration. It validates the data using the `RegisterSerializer` and creates a new user.
- **`LoginView`** authenticates the user using the provided email and password, then generates and returns **JWT tokens** (access and refresh).
- **`UserInfoView`** retrieves information about the currently logged-in user.

---

## 4. JWT Authentication Settings

To enable JWT authentication, we need to install `djangorestframework-simplejwt` and configure it in Django settings.

### Install the required package:

```bash
pip install djangorestframework-simplejwt
```

### Update `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    ...
]

AUTH_USER_MODEL = 'api.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

---

## 5. URL Configuration

To expose the authentication views, include them in the `urls.py` of the backend.

### **`urls.py`**

```python
from django.urls import path
from .views import RegisterView, LoginView, UserInfoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserInfoView.as_view(), name='user_info'),
]
```

### Explanation:
- **`register/`**: Endpoint for registering a user.
- **`login/`**: Endpoint for logging in and getting JWT tokens.
- **`user/`**: Endpoint for getting the current user's info (requires a valid JWT token).

---

## 6. Testing the Endpoints with Postman

1. **Register User**:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/register/`
   - Body (JSON):
   ```json
   {
       "username": "adminuser",
       "email": "admin@example.com",
       "password": "adminpassword",
       "is_admin": true
   }
   ```
   
2. **Login User**:
   - Method: `POST`
   - URL: `http://127.0.0.1:8000/api/login/`
   - Body (JSON):
   ```json
   {
       "email": "admin@example.com",
       "password": "adminpassword"
   }
   ```
   - Response:
   ```json
   {
       "refresh": "<refresh_token>",
       "access": "<access_token>"
   }
   ```

3. **Get User Info** (with JWT Token):
   - Method: `GET`
   - URL: `http://127.0.0.1:8000/api/user/`
   - Headers: `Authorization: Bearer <access_token>`

---

## Conclusion

In this stage, we implemented:
- A **custom user model** with `is_admin` field and unique `email`.
- **JWT authentication** for user registration, login, and fetching user info.
- Postman was used for testing endpoints.

---

With this setup, users can register, log in, and get their info, while also assigning the admin role using the `is_admin` field.

from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.get(email='admin@example.com')
print(user.admin@example.com)  # should be the same as email
print(user.check_password('admin'))
# Repository for Django/DRF Connectly Project

## Install Python and Extensions in VS Code

1. Create a folder where you will place the **connectly_project**, for this demo we will call it api
2. Check if Python is Installed
   Run the following command in your terminal:
   python --version
   This should display the installed Python version (e.g., Python 3.10.5).
   If not, download and install the latest version of Python from python.org.
3. Install pip **(don’t skip this step)**
   Ensure pip (Python's package manager) is installed:
   pip --version
   If not, install it using:
   python -m ensurepip --upgrade
4. Set Up a Virtual Environment **(don’t skip this step)**
   a. A virtual environment keeps your project dependencies isolated from the global Python environment.
   b. Create the Virtual Environment
   i. Navigate to your project folder in the terminal and run:
   python -m venv env
   This creates a virtual environment named env.
5. Activate the Virtual Environment:
   On Windows:
   .\env\Scripts\activate
   On MacOS/Linux:
   source env/bin/activate
6. Verify the Virtual Environment
   python --version
   You should see the same Python version, but the terminal prompt will include (env) to indicate the environment is active.

## Setting Up the Django Project

1.  Make sure Python is installed.
2.  Install Django and Django REST Framework

    a. Install Django:
    Run:
    pip install django
    b. Verify the installation:
    django-admin --version

    c. Install Django REST Framework (DRF)
    Run:
    pip install djangorestframework

3.  Install the required tools for testing and admin functionality:

    pip install djangorestframework-simplejwt
    pip install django-cors-headers

4.  Create the Django Project
    a. Run the following command to create a Django project named connectly_project:
    django-admin startproject connectly_project
5.  Navigate to the Project Directory
    cd connectly_project
6.  This will generate the necessary project files, including settings.py.
7.  Configure Django REST Framework
    a. Add rest_framework to Installed Apps:
    i. Open connectly_project/settings.py and add 'rest_framework' to the INSTALLED_APPS list:
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # Add Django REST Framework
    ]

8.  Set Up the Database: **(skip)**
    Django uses SQLite by default, which is ideal for development. You don’t need to make any changes to the database settings at this point.

9.  Run Initial Migrations:
    a. Migrations are a way to apply database schema changes, creating tables for your models in the database based on your configurations:
    python manage.py migrate
10. Verify Django REST Framework Setup
    a. Create Basic URL Routes:
    b. Open connectly_project/urls.py and add a route for the DRF browsing interface:

        from django.contrib import admin
        from django.urls import path, include


        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
        ]

        Note: Adding this URL route enables DRF's built-in login/logout functionality for testing API endpoints that require authentication.
        Test the Setup:
        Restart the development server if it’s not running, in the terminal run the command:
        python manage.py runserver
        Navigate to http://127.0.0.1:8000/api-auth/login/ to see the DRF login interface. This confirms that DRF is installed and configured.

## Configuring Models

1.  Navigate to connectly_project directory
    cd connectly_project
2.  Create the posts App
    a. In the terminal, create the app:
    python manage.py startapp posts
    b. Register the app in connectly_project/settings.py:
    INSTALLED_APPS = [
    ...,
    'posts',
    ]
3.  Define Models
    a. In posts/models.py, define the User and Post models with validation to ensure data integrity.

        from django.db import models


        class User(models.Model):
            username = models.CharField(max_length=100, unique=True)  # User's unique username
            email = models.EmailField(unique=True)
            created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created


            def __str__(self):
                return self.username

## Apply Migrations

1. Open new terminal in VS Code and create migration files: (don’t skip this step)
   python manage.py makemigrations
2. Apply the migrations:
   python manage.py migrate

## Defining CRUD Operations in Views

**Note: If you have downloaded the source code for repository, you may skip this section since they're already included**

1. In posts/views.py, implement views with basic error handling for common issues, such as invalid IDs or duplicate data.
2. Retrieve All Users (GET):
   from django.http import JsonResponse
   from .models import User

   def get_users(request):
   try:
   users = list(User.objects.values('id', 'username', 'email', 'created_at'))
   return JsonResponse(users, safe=False)
   except Exception as e:
   return JsonResponse({'error': str(e)}, status=500)

3. Create a User (POST):
   import json
   from django.http import JsonResponse
   from django.views.decorators.csrf import csrf_exempt
   from .models import User

   @csrf_exempt
   def create_user(request):
   if request.method == 'POST':
   try:
   data = json.loads(request.body)
   user = User.objects.create(username=data['username'], email=data['email'])
   return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201)
   except Exception as e:
   return JsonResponse({'error': str(e)}, status=400)

4. Update a User (PUT)
   @csrf_exempt
   def update_user(request, id):
   if request.method == 'PUT':
   try:
   data = json.loads(request.body)
   email = data['email']
   user = User.objects.filter(id=id).first() # data = UserSerializer(isinstance=user, data=request.data)
   user.email = email
   user.save()
   return JsonResponse({'message': 'User updated successfully'}, status=201)
   except Exception as e:
   return JsonResponse({'error': str(e)}, status=400)

5. Delete a User (DELETE)
   @csrf_exempt
   def delete_user(request, id):
   if request.method == 'DELETE':
   try:
   user = User.objects.filter(id=id).first()
   user.delete()
   #User.objects.delete(id=id)
   return JsonResponse({'message': 'User deleted successfully'}, status=200)
   except Exception as e:
   return JsonResponse({'error': str(e)}, status=400)

## Mapping URLs to Endpoints

1.  Create a **urls.py** File for the posts App
    a. In posts/urls.py, define the URL patterns for the views.

        from django.urls import path
        from . import views

        urlpatterns = [
            path('users/', views.get_users, name='get_users'),
            path('users/create/', views.create_user, name='create_user'),
            path('users/update/<int:id>/', views.update_user, name='update_user'),
            path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
        ]

2.  Include posts App URLs in the Project
    a. Update connectly_project/urls.py to include the posts app URLs.
    from django.contrib import admin
    from django.urls import path, include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('api-auth/', include('rest_framework.urls')),
            path('posts/', include('posts.urls')),
        ]

## Testing API Functionality Using Postman

1. Setup Postman:
2. Download and install Postman, if you haven't already.
3. Open Postman and create a new request.
4. Ensure the Django development server is running, if not restart your server by executing:
   python manage.py runserver
5. Use the server URL http://127.0.0.1:8000 for all requests.
   a. Test GET /posts/users/
   **example**: http://127.0.0.1:8000/posts/users/
   b. Test POST /posts/users/create/
   **example**: http://127.0.0.1:8000/posts/users/create/
   the request body should contain the following json format:
   {
   "username": "use1",
   "email": "user1@example.com"
   }

   c. Test PUT /posts/users/update/
   **example**: http://127.0.0.1:8000/posts/users/update/2/
   the request body should contain the following json format:
   {
   "email": "newuser2@example.com"
   }
   d. Test DELETE /posts/users/delete/
   **example**: http://127.0.0.1:8000/posts/users/delete/2/



## Branch 4 instructions
1. Check out branch-week4-demo branch
2. Run the python command below to install Django argon2 password hasher 
    pip install django[argon2]
3.  Run the python command below to install bcrypt for pasword salting
    pip install bcrypt
4. Run the python command below to install Django SSL server
    pip install django-sslserver
5. Migrate additional extensions
    a. python manage.py makemigrations posts
    b. python manage.py migrate
6. Running the server
    python manage.py runsslserver —-certificate cert.pem —-key key.pem


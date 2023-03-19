# TalkZone

TalkZone is a web application like Tinder but it uses text instead of photos. It is developed by TTN team using Django REST framework as the backend service.

## Description

TalkZone allows users to write anything like Twitter in different categories. Others can see this text file and if they like it, they can start a conversation with the author. It uses Django channels for chat implementation and PostgreSQL as database.

## Installation

- First you need to install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

- Then you need to create a PostgreSQL database and configure the settings.py file with the database credentials. You also need to run the migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Note: Because of a bug in swagger package, you have to follow this instruction before using the browsable API:

`Navigate to index.html ({PYTHON PATH}\site-packages\rest-framework-swagger\index.html)`

`Change second line {% load staticfiles %} to {% load static %}`

## Usage

To run TalkZone, you need to start the Django development server:

>$ python manage.py runserver

Then you can access the web application at http://localhost:8000/ and the browsable API at http://localhost:8000/api/. You can also use the admin interface at http://localhost:8000/admin/ with your superuser credentials.

Check http://localhost:8000/api_documentation/ for Document and Management

Check http://localhost:8000/admin/ for Database Management

<b><i> APP_NAME </i></b>

# Instructions For Use

<b> clone project </b>

## PostgreSQL
Download Link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Create a Database (Check ttn_web/settings.py for database name)
- create a Login/Group Roles (Check ttn_web/settings.py for user and password)

## Virtualenv

#### Install Virtualenv
> $ pip install virtualenv

#### Create your enviremant
> $ cd PATH_TO_PROJECT

> $ pip -m venv YOUR_ENVIREMENT_NAME

#### Enviremant activation
> $ .\YOUR_ENVIREMENT_NAME\Scripts\activate

## Requirements

#### Install requirements
> $ pip install -r requirements.txt

`Navigate to index.html ({PYTHON PATH}\site-packages\rest-framework-swagger\index.html)`

`Change second line {% load staticfiles %} to {% load static %}`

#### Download and Install Memurai

Download from: https://www.memurai.com/

##

#### Migrate your project
>$ python manage.py migrate

#### Create your super user
>$ python manage.py createsuperuser

#### Start project
>$ python manage.py runserver

Login with your created super http://localhost:8000/admin/

Check http://localhost:8000/api_documentation/ for Document and Management

Check http://localhost:8000/admin/ for Database Management
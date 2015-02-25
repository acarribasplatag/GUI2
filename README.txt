https://www.djangoproject.com/download/ - install django python

start server : "python manage.py runserver" from GUI2 directory
localhost:8000 - mainpage, once server is running type this url into browser

"python manage.py migrate" updates your database

"python manage.py createsuperuser" creates an admin account
go to "localhost:8000/admin" to see the database, you can add to it directly here

mysite - contains settings for the website

polls is an app apps. An app contains parts of the website with similar functionality.

Each app has a models.py file. 
This contains the database classes needed for each individual app.

templates - contains the html templates
static - contains css and javascript for the template files

urls - handles the urls for each app
views - passed database information to the html templates. For example when a user loads
a topic views will pass the information needed to build the page to the template file from
the database.

"python manage.py startapp polls" creates a new app

source venv/bin/activate - runs from virtual environment (server uses this environment)
here you can install stuff that the server will need

sudo pip freeze > requirements.txt - this outputs all the dependancies to requirements.txt 
sudo pip install -r requirements.txt - installs required dependancies needed

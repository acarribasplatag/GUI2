*** First Time Setup ***
https://www.djangoproject.com/download/ - install django python
"sudo apt-get install python-dev" - install python dev tools
"sudo apt-get install python-pip" - install pip (manages python packages)
sudo pip install -r requirements.txt - installs required dependancies needed

*** Start Server ***
start server : "python manage.py runserver" from GUI2 directory
localhost:8000 - mainpage, once server is running type this url into browser

*** Update database (after changing models.py) ***
"python manage.py makemigrations appname(polls, registration)" 
"python manage.py migrate" updates your database

*** Create an admin account ***
"python manage.py createsuperuser" creates an admin account
go to "localhost:8000/admin" to see the database, you can add to it directly here

*** Where is everything ***
mysite - contains settings for the website
polls is an app apps. An app contains parts of the website with similar functionality.
polls app contains stuff relatiing to polls
registration app contains stuff relating to users

*** How stuff works ***
url.py - determines what happens when you go to a paticular url (every app has their own url.py)
view.py - python functions. Typically a url calls a function in your view.py file.
templates - contains html files for the website. view.py functions render these templates. Most templates inherit from base.html.
static - contains css/javascript/images
(url.py -> view.py method -> template)

models.py - contains the database objects.
admin.py - models in here can be accessed from the admin page.

templates - contains the html templates
static - contains css and javascript for the template files

*** create a new app ***
"python manage.py startapp polls" creates a new app

*** run code from virtual enviornment ***
source venv/bin/activate - runs from virtual environment (server uses this environment)
here you can install stuff that the server will need

*** Install new requirements ***
source venv/bin/activate (switch to virtual enviornment) sudo pip install (new package) - this is how you would install new packages to use on the site.
sudo pip freeze > requirements.txt - this outputs all the dependancies to requirements.txt (should only be done from virtual enviornment)
sudo pip install -r requirements.txt - installs required dependancies needed

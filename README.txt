*** First Time Setup ***
https://www.djangoproject.com/download/ - install django python
"sudo apt-get install python-dev" - install python dev tools
"sudo apt-get install python-pip" - install pip (manages python packages)
pip install -r requirements.txt - installs required dependancies needed
python manage.py makemigrations polls - build database for polls app
python manage.py makemigrations registration - build database for registration app
python manage.py migrate - initial migration

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

*** Install new dependancies ***
sudo pip install -r requirements.txt - installs required dependancies needed

*** Add new packages to the site ***
source venv/bin/activate (switch to virtual enviornment, the server runs off this enviornment) 
sudo pip install (new package) - this is how you would install new packages to use on the site.
sudo pip freeze > requirements.txt - this outputs all the dependancies to requirements.txt so other developers can quickly install them\

*** How to use github *** 
(get new code)
git fetch upstream
git merge upstream/master

(put your updated code on YOUR github)
git add --all
git commit -m "message telling what you did"
git push origin/master (master is the branch) ("git branch" tells what branch you are on)

(create a pull request, this will move your updated code from your github to upstream (bobbys github))
you need to go to your github account on www.github.com and click the pull request button.




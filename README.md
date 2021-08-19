# Covid Tracking and Exposure Predictions Application
This is a python project developed with the aim of allowing people to learn their covid exposure rates by providing an analysis of individual health and travel histories that a person will provide through the app. It also gives information on useful next steps for keeping safe and protecting oneself against the covid-19 virus.

# To install and run the project on your local machine:
1. Clone this repo.
2. Change into the project directory by running _cd covidTracker_
3. Create a project virtual environment.
4. Run _pip install -r requirements.txt_ from the project root directory.
5. Create a postgres database with the name _covidtracker_ as defined in the settings.py file. 
If you create a database with a different name update settings.py under the section with DATABASES = { 
Change the line with _'NAME': 'covidtracker'_
6. Set up a database user
7. Then run _python manage.py migrate_. If you have python3 run _python3 manage.py migrate_
8. Create an admin account by running the command: _python manage.py createsuperuser_
9. Make database migrations using the command: _python manage.py makemigrations_
10. To apply these migrations run _python manage.py migrate_
11. Finally, run the development server using _python manage.py runserver_ and open _127.0.0.1:8000_ on your browser to view the app.

# Built With
- HTML
- CSS/Bootstrap
- Python/Django
- Javascript
- Postman Covid-19 API

# You can view project progress via:
covidtrackerdjango.herokuapp.com


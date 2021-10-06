## Covid Tracking and Exposure Predictions Application
This is a python project developed with the aim of allowing people to learn their covid exposure rates by providing an analysis of individual health and travel histories that a person will provide through the app. It also gives information on useful next steps for keeping safe and protecting oneself against the covid-19 virus.

### To install and run the project on your local machine:
1. Clone this repo.
2. Change into the project directory by running:
```bash
cd CovidTracker
```
3. Create a project virtual environment.

4. Run the following command from the project root directory 
```bash
pip install -r requirements.txt
 ```
7. Create a postgres database with the name _covidtracker_ as defined in the settings.py file. 
If you create a database with a different name update settings.py under the section with DATABASES = { 
Change the line with _'NAME': 'covidtracker'_

8. Set up a database user

9. Next, run:
```bash
python manage.py migrate
 ```

10. Create an administrator account by running the command:
```bash
python manage.py createsuperuser
```
11. Make database migrations using the command: 
```bash
python manage.py makemigrations
```
12. To apply these migrations run
```bash
python manage.py migrate
```
13. Finally, run the development server using:
```bash
python manage.py runserver
```
14. Enter _http://127.0.0.1:8000_ on your browser to view the app.

# Built With
- HTML/CSS/Javascript/Bootstrap
- Django framework
- Postman Covid-19 API

# You can view project progress via:
covidtrackerdjango.herokuapp.com


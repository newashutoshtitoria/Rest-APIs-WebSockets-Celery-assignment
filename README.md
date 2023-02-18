## Assignment
    Task1:
    (Backend Only, Preferably Django Rest Framework)
    Rest APIs, WebSockets, Celery
    Create and Django App-
    1. Users can signup and sign in.
    2. Users can upload images, via celery task.
    3. Users can like images and fulfill all required operations such as-
        ○ Only authenticated users can like an image.
        ○ Only one time the user can like an image.
        ○ Notification send to the user whose image was liked by other
        users.
        ○ Authenticated User can get the list of all the images posted
        by other users in a single query just by that user id.
        ○ When any user queries an image or image list of the other
        users, there should be one more field, that is liked (True or
        False), if the user has liked that image then this field should
        be True in its JSON.
    4. Schedule notification for every 4 hours from the last API call time.

### Setup...
    git clone https://github.com/Neerajsinghtanwar/Assignment.git
    cd assignment

### Create a virtual environment to install dependencies in and activate it...
    virtualenv venv
    source env/bin/activate

### Then install the dependencies...
    (venv)$ pip install -r requirements.txt

### Once pip has finished downloading the dependencies...
    (venv)$ python manage.py runserver

### Run celery worker command in 2nd terminal...
    celery -A assignment worker -l INFO

### Run celery beat command in 3rd terminal...
    celery -A assignment beat -l INFO

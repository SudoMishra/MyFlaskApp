# Readme for Flask App

1. The folder structure is as follows.
```console
.
├── Readme.md
├── MyFlaskApp.conf
├── MyFlaskApp.wsgi
├── __init__.py
├── app
│   └── mnist.py
├── auth
│   └── routes.py
├── celerybeat.conf
├── config.ini
├── db.sqlite
├── flask_app.py
├── logs
│   ├── errlogfile.log
│   └── logfile.log
├── models.py
├── requirements.txt
├── static
│   ├── models
│   │   └── mnist_model_1.hdf5
│   └── uploads
│       ├── 0.png
│       ├── 1.png
│       ├── 10.png
│       ├── 2.png
│       ├── 3.png
│       ├── 4.png
│       ├── 5.png
│       ├── 6.png
│       ├── 7.png
│       ├── 8.png
│       ├── 9.png
│       ├── alt1.png
│       ├── alt_6.png
│       ├── alt_6_1.png
│       └── alt_6_2.png
├── supervisord.conf
├── tasks.py
└── templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── predict.html
    └── signup.html
```
1. The flask app allows a user to sign up and register their profiles in the SqlAlchemy Database.
2. In the predict page the user can upload an image of a digit. 
3. The user can then use the predict button to get a prediction about the uploaded image.
4. The app can be run on a flask server as well as a wsgi server.
5. There is a test.ini file that contains the config for a uwsgi server.
6. The app can be deployed on the uwsgi server using the following command
    ```console
    uwsgi config.ini
    ```
7. The app can be run through supervisor as well. The supervisord.conf has the config details.
8. Point supervisor to read the config file using the following command,
    ```console
        supervisord -c supervisord.conf
    ```
9. To watch updates regarding supervisor,
    ```console
        supervisorctl
    ```
10. The uploaded images are stored in the `static/uploads` folder
11. The model is also stored in the `static/models` folder
12. The Jinja templates for the html files are stored in the `templates` folder
13. The `static/uploads` folder already contains a couple of mnist like images.
14. To run the app using mod_wsgi
    ```console
        mod_wsgi start-server MyFlaskApp.wsgi
    ```
15. The `app/` folder contains `mnist.py` which handles the main upload and predict tasks of the app.
16. The `auth/` folder contains `routes.py` which handle logging and signup tasks of the app.
17. `flask_app.py` creates and initializes the flask app.

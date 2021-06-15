# fynd_imdb

In this repo I've tried to implement a simple CRUD API in python sanic lightweight framework.
To run this project: 

  1. Git clone repo
  2. create a virtual environment.
  3. activate virtual env.
  4. pip install -r requirements.txt
  5. install mongodb and create database. (optional: you can use Atlas cluster too.)
  6. create config.ini file in same project folder.
  
  ```
    [main]
    SECRET_KEY = your secret key
    DEBUG = True/False

    [database]
    MONGODB_URL = mongodb://localhost:27017/db_name or connection url of your Atlas cluster.

    [logging]
    folder = /var/log/imdb_logs

  ```
  7. run: python app.py

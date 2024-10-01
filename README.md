# flask_email_scheduler

## How to run
Make sure you already installed **python3.8** or higher in your machine

1. Create your virtualenv and activate (if you are using virtuanenv)
2. Install library 
    ```sh
    pip install -r requirements.txt
    ```
   
3. copy .env.example to .env
    ```sh
    cp .env.example .env
    ```
    
5. run migraton file
    ```sh
    flask db upgrade
    ```
   
7. run server flask
    ```sh
    # maske sure your root terminal is */core-tcico/
    # run locally
    flask run --port 5003

    # run in server
    flask run --host=0.0.0.0 --port=5003
    ```
   
8. run server celery worker
    ```sh
    # create new terminal and activate the virtualenv
    # celery worker
    celery -A server.celery worker --loglevel INFO

    # celery worker on windows user, `--pool solo`
    celery -A server.celery worker --pool solo --loglevel INFO
    ```

9. run server celery beat (scheduler)
    ```sh
    # create new terminal and activate the virtualenv
    # make sure step 8 executed

    # celery beat
    celery -A server.celery beat --loglevel INFO
    ```
   
10. run celery flower (monitoring task)
   ```sh
  celery -A proj flower --address=127.0.0.1 --port=5566
   ```


### How to set connection DB
Set your .env file for variable key for `SQLALCHEMY_DATABASE_URI` 
<br> ex : `postgresql://postgres:postgres@localhost/emaildb`
<br><br>

### How to Manage ORM DB 
1. only for the first time, when you create migration file
    ``` sh
    flask db init
    ```
2. make migrate file (alembic), for any change in your models
    ``` sh
    flask db migrate -m 'custom_message'
    ```
    <br> re-check your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.
3. execute migration for your change in db
    ``` sh
    flask db upgrade
    ```

    after make ORM class for table [`path: ./models]
<br> make sure your ORM class is registered in variable register_tables
[`path: ./models.py`]
<br> if your new ORM class is not registered yet, you cann't migrate your db
<br><br>


2. Use pytest
<br> You can run unit test by executing this command
``` sh
# run all unittest
pytest or pytest -q tests --disable-warnings

# run single file
pytest or pytest -q tests/test_email.py --disable-warnings

# run single unittest function
pytest -q tests/test_email.py -k test_routes --disable-warnings

```
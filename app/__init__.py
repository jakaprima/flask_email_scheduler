from flask import Flask, request, jsonify
from flask_dotenv import DotEnv
# from .models import db
from .email.views import bp_email
from . import extensions
from .models import db, register_tables
from apscheduler.schedulers.background import BackgroundScheduler
from celery import Celery, Task
from .config import app_settings

# ---------------------------- INIT APP
def create_app(environment=None):
    app = Flask(__name__)
    # Load environment variables from .env file
    dotenv = DotEnv()
    dotenv.init_app(app)

    if environment == 'testing':
        selected_app_settings = app_settings.get('testing')
    else:
        selected_app_settings = app_settings.get(app.config.get('FLASK_ENV', 'development'))
    app.config.from_object(selected_app_settings)

    # set secret_key
    app.secret_key = app.config['SECRET_KEY']

    # register extensions
    register_extensions(app)

    # Create the database tables
    with app.app_context():
        extensions.db.create_all()
    # register blueprint
    register_blueprints(app)

    register_shellcontext(app)

    return app

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(bp_email)
    return None

def register_extensions(app):
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.mail.init_app(app)
    extensions.ma.init_app(app)
    return None

def register_shellcontext(app):
    """Register shell context objects."""
    shell_context = {
        'db': extensions.db
    }
    shell_context.update(register_tables)
    def shell_context():
        """Shell context objects."""
        return shell_context

    app.shell_context_processor(shell_context)

def make_celery(app):
    is_log_console = True
    selected_app_settings = app_settings.get(app.config.get('FLASK_ENV', 'development'))
    if selected_app_settings.CELERY_LOG_TYPE == "file":
        is_log_console = False

    celery = Celery(
        'core_email_scheduler',
        broker=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        include=['app.tasks'],
        enable_utc=True,
        timezone=app.config['CELERY_TIMEZONE'],
        worker_hijack_root_logger=is_log_console
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_worker_app():
    """create worker app without blueprint"""
    app = Flask(__name__)
    selected_app_settings = app_settings.get(app.config.get('FLASK_ENV', 'development'))
    app.config.from_object(selected_app_settings)
    app.logger.setLevel(selected_app_settings.LOG_LEVEL)
    register_extensions(app)
    register_shellcontext(app)

    return app

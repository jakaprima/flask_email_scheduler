from app import (create_app, )
from app import (make_celery, create_worker_app)

# ----------------------------- init app
app = create_app()
celery = make_celery(create_worker_app())

# service-brand-api

gunicorn app:app --log-level DEBUG --reload --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9001 --timeout 360
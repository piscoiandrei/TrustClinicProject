web: daphne trust_clinic.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=trust_clinic.settings -v2
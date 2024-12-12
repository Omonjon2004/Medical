import os
from celery import Celery

# Django settings modulini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Medical')

# Redisni Celery brokeri sifatida sozlash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery tasklarini topish
app.autodiscover_tasks()

# Redisga ulangan broker
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'



app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# import os
# from celery import Celery
#
# # Django settings modulini sozlash
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# app = Celery('Medical')
#
# # Django settings-dan konfiguratsiyalarni o'qish
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Redis broker va backend
# app.conf.broker_url = 'redis://localhost:6379/0'  # Tasklar uchun broker
# app.conf.result_backend = 'redis://localhost:6379/0'  # Task natijalarini saqlash uchun backend
#
#
# # Celery 6.0 uchun yangi retry opsiyasi
# app.conf.broker_connection_retry_on_startup = True
#
# # Tasklarni avtomatik topish
# app.autodiscover_tasks()
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
# import os
# from celery import Celery
#
# # Django settings modulini sozlash
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# # Celery app yaratish
# app = Celery('Medical')
#
# # Django konfiguratsiyalarini yuklash
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Tasklarni avtomatik topish
# app.autodiscover_tasks()
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django settings modulini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery app yaratish
app = Celery('Medical')

# Django sozlamalarini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tasklarni avtomatik topish
app.autodiscover_tasks()

# Brokerga ulanishga urinishlarni faollashtirish (Retry on startup)
app.conf.broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

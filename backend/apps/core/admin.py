from django.contrib import admin
from .models import Athlete, Session, SensorSample

admin.site.register(Athlete)
admin.site.register(Session)
admin.site.register(SensorSample)

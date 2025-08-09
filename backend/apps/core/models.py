from django.db import models
from django.conf import settings

class Athlete(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    started_at = models.DateTimeField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    raw_file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return f"Session {self.id} — {self.athlete} — {self.started_at.date()}"

class SensorSample(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='samples')
    timestamp = models.DateTimeField()
    sensors = models.JSONField()

    class Meta:
        indexes = [models.Index(fields=['session', 'timestamp'])]

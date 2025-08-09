import csv
import io
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.models import Session, SensorSample, Athlete
from django.http import JsonResponse

class UploadCSVView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'frontend/upload.html')

    def post(self, request):
        csvfile = request.FILES.get('file')
        athlete_id = request.POST.get('athlete_id')
        started_at = request.POST.get('started_at')
        if not csvfile:
            return JsonResponse({'error': 'no file'}, status=400)
        athlete = Athlete.objects.get(id=athlete_id)
        session = Session.objects.create(
            athlete=athlete,
            started_at=started_at or datetime.now(),
            raw_file=csvfile,
        )

        text = csvfile.read().decode('utf-8')
        reader = csv.reader(io.StringIO(text))
        headers = next(reader)
        for row in reader:
            ts_str = row[0]
            try:
                ts = datetime.fromisoformat(ts_str)
            except Exception:
                ts = session.started_at + timedelta(seconds=float(ts_str))
            sensors = {f's{i}': float(val) if val else None for i, val in enumerate(row[1:])}
            SensorSample.objects.create(session=session, timestamp=ts, sensors=sensors)

        return redirect('upload')

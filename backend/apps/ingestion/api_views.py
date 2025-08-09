from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.core.models import Session, Athlete, SensorSample
import csv, io
from datetime import datetime

class CSVUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        f = request.FILES.get('file')
        athlete_id = request.data.get('athlete_id')
        if not f or not athlete_id:
            return Response({'detail': 'file and athlete_id required'}, status=400)

        athlete = Athlete.objects.get(pk=athlete_id)
        session = Session.objects.create(athlete=athlete, started_at=datetime.now(), raw_file=f)

        text = f.read().decode('utf-8')
        reader = csv.reader(io.StringIO(text))
        headers = next(reader, None)
        for row in reader:
            ts = datetime.fromisoformat(row[0])
            sensors = {f's{i}': float(v) if v else None for i, v in enumerate(row[1:])}
            SensorSample.objects.create(session=session, timestamp=ts, sensors=sensors)

        return Response({'session_id': session.id})

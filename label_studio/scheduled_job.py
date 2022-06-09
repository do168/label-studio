import os
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.label_studio")
import django

django.setup()

# from schs import models as schmodel
from schs import api as scapi
from ml.api import SchMLBackendInteractiveAnnotating

sch_api = scapi.SchListAPI()  # schedule instance
ml_api = SchMLBackendInteractiveAnnotating()  # mlbackend instance
schs = sch_api.get_queryset_all()  # 모든 스케줄 가져오기

now = datetime.now()  # 현재 시간 계산
for sch in schs:
    period = sch.period
    if sch.updated_at + timedelta(hours=period) > now:  # 스케줄 마지막 갱신 시간 + 주기 > 현재 시간
        ml_api.post(pk=sch.model.id, projectId=sch.project.id)  # prediction

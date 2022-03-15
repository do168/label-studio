"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import drf_yasg.openapi as openapi
import logging
import numpy as np
import pathlib
import os

from collections import Counter
from django.db import IntegrityError
from django.db.models.fields import DecimalField
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.db.models import Q, When, Count, Case, OuterRef, Max, Exists, Value, BooleanField
from rest_framework import generics, status, filters
from rest_framework.exceptions import NotFound, ValidationError as RestValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import exception_handler

from core.utils.common import conditional_atomic, temporary_disconnect_all_signals
from core.label_config import config_essential_data_has_changed
from projects.models import (
    Project, ProjectSummary, ProjectManager
)
from projects.serializers import (
    ProjectSerializer, ProjectLabelConfigSerializer, ProjectSummarySerializer
)
from tasks.models import Task, Annotation, Prediction, TaskLock
from tasks.serializers import TaskSerializer, TaskSimpleSerializer, TaskWithAnnotationsAndPredictionsAndDraftsSerializer
from webhooks.utils import api_webhook, api_webhook_for_delete, emit_webhooks_for_instance
from webhooks.models import WebhookAction

from core.permissions import all_permissions, ViewClassPermission
from core.utils.common import (
    get_object_with_check_and_log, bool_from_request, paginator, paginator_help)
from core.utils.exceptions import ProjectExistException, LabelStudioDatabaseException
from core.utils.io import find_dir, find_file, read_yaml

from data_manager.functions import get_prepared_queryset, filters_ordering_selected_items_exist
from data_manager.models import View

from label_studio.projects.api import ProjectListAPI
from label_studio.tasks.api import TaskListAPI

import label_studio.projects.api

logger = logging.getLogger(__name__)


class ProjectListPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'


@method_decorator(name='get', decorator=swagger_auto_schema(
    tags=['Projects'],
    operation_summary='List your projects',
    operation_description="""
    Return a list of the projects that you've created.

    To perform most tasks with the Label Studio API, you must specify the project ID, sometimes referred to as the `pk`.
    To retrieve a list of your Label Studio projects, update the following command to match your own environment.
    Replace the domain name, port, and authorization token, then run the following from the command line:
    ```bash
    curl -X GET {}/api/projects/ -H 'Authorization: Token abc123'
    ```
    """.format(settings.HOSTNAME or 'https://localhost:8080')
))
@method_decorator(name='post', decorator=swagger_auto_schema(
    tags=['Projects'],
    operation_summary='Create new project',
    operation_description="""
    Create a project and set up the labeling interface in Label Studio using the API.

    ```bash
    curl -H Content-Type:application/json -H 'Authorization: Token abc123' -X POST '{}/api/projects' \
    --data "{{\"label_config\": \"<View>[...]</View>\"}}"
    ```
    """.format(settings.HOSTNAME or 'https://localhost:8080')
))
class TritonApi(generics.ListCreateAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    serializer_class = ProjectSerializer
    filter_backends = [filters.OrderingFilter]
    permission_required = ViewClassPermission(
        GET=all_permissions.projects_view,
        POST=all_permissions.projects_create,
    )
    ordering = ['-created_at']
    pagination_class = ProjectListPagination

    def perform_create(self, ser):
        try:
            project = ser.save(organization=self.request.user.active_organization)
        except IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: project.title, project.created_by_id':
                raise ProjectExistException('Project with the same name already exists: {}'.
                                            format(ser.validated_data.get('title', '')))
            raise LabelStudioDatabaseException('Database error during project creation. Try again.')

    def post(self, request, *args, **kwargs):
        logger.error(self.request.data)
        project_list_api = ProjectListAPI()
        title = "Created from Auto-labeling"
        label_config = '''<View><Image name="image" value="$image"/><RectangleLabels name="label" 
        toName="image"><Label value="obj" background="#FFA39E"/></RectangleLabels></View> '''
        project_request_data = {"title": title, "label_config": label_config}
        data = project_list_api.post(project_request_data)

        task_list_api = TaskListAPI()

        task_request_data = {
            'data': {'image': '/data/local-files/?d=test/273275,5f45d0002d92d1b5.jpg'},
            'annotations': [{
                'result': [{
                    "original_width": 480,
                    "original_height": 717,
                    "image_rotation": 0,
                    "value": {
                        "x": 6.25,
                        "y": 43.793584379358435,
                        "width": 77.29166666666667,
                        "height": 39.05160390516039,
                        "rotation": 0,
                        "rectanglelabels": [
                            "Car"
                        ]
                    },
                    'from_name': 'label',
                    'to_name': 'image',
                    'type': 'rectanglelabels',
                    'origin': 'prediction'
                }],
                'score': 0.87
            }]
        }

        task_list_api.post(task_request_data)

    # def add_result(annotations):
    #     # original_width, original_height, image_rotation, x, y, width, height, rotation, rectanglelabels
    #     result = {}
    #     # result['original_width'] = 480
    #     result['original_width'] = annotations['original_width']
    #     # result['original_height'] = 717
    #     result['original_height'] = annotations['original_height']
    #     # result['image_rotation'] = 0
    #     result['image_rotation'] = annotations['image_rotation']
    #     result['value'] = {}
    #     # result['value']['x'] = 6.25
    #     result['value']['x'] = annotations['x']
    #     # result['value']['y'] = 43.79
    #     result['value']['y'] = annotations['y']
    #     # result['value']['width'] = 77.29
    #     result['value']['width'] = annotations['width']
    #     # result['value']['height'] = 39.05
    #     result['value']['height'] = annotations['height']
    #     # result['value']['rotation'] = 0
    #     result['value']['rotation'] = annotations['rotation']
    #     # result['value']['rectanglelabels'] = ['car']
    #     result['value']['rectanglelabels'] = annotations['rectanglelabels']
    #     result['from_name'] = 'label'
    #     result['to_name'] = 'image'
    #     result['type'] = 'rectanglelabels'
    #     result['origin'] = 'prediction'
    #     return result
    #
    # def add_annotation(res):
    #     # image_path, score
    #     datas = {}
    #     datas['data'] = {}
    #     # datas['data']['image'] = '/data/local-files/?d=KISA_NORMAL_DB/video_test1_no_1_img_0003.png'
    #     datas['data']['image'] = res['image_path']
    #     datas['predictions'] = []
    #
    #     results = {}
    #     results['result'] = []
    #     # results['score'] = 0.87
    #     results['score'] = res['score']
    #
    #     for res_ in res['annotations']['results']:
    #         results['result'].append(add_result(res_))
    #     datas['predictions'].append(results)
    #     return datas
    #
    # def make_results_to_json(results):
    #     meta_result = []
    #
    #     for res in results:
    #         meta_result.append(add_annotation(res))
    #
    #     # print(json.dumps(meta_result))
    #     return meta_result




"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
from core.label_config import generate_sample_task_without_check
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from users.serializers import UserSimpleSerializer

from projects.models import Project, ProjectOnboarding, ProjectSummary

"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import os
import ujson as json

from rest_framework import serializers
from django.db import transaction


from data_manager.models import View, Filter, FilterGroup
from tasks.models import Task
from tasks.serializers import TaskSerializer, AnnotationSerializer, PredictionSerializer, AnnotationDraftSerializer
from projects.models import Project
from label_studio.core.utils.common import round_floats


class CreatedByFromContext:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('created_by')


class ProjectSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """ Serializer get numbers from project queryset annotation,
        make sure, that you use correct one(Project.objects.with_counts())
    """

    task_number = serializers.IntegerField(default=None, read_only=True,
                                        help_text='Total task number in project')
    total_annotations_number = serializers.IntegerField(default=None, read_only=True,
                                                    help_text='Total annotations number in project including '
                                                              'skipped_annotations_number and ground_truth_number.')
    total_predictions_number = serializers.IntegerField(default=None, read_only=True,
                                                    help_text='Total predictions number in project including '
                                                              'skipped_annotations_number, ground_truth_number, and '
                                                              'useful_annotation_number.')
    useful_annotation_number = serializers.IntegerField(default=None, read_only=True,
                                                     help_text='Useful annotation number in project not including '
                                                               'skipped_annotations_number and ground_truth_number. '
                                                               'Total annotations = annotation_number + '
                                                               'skipped_annotations_number + ground_truth_number')
    ground_truth_number = serializers.IntegerField(default=None, read_only=True,
                                            help_text='Honeypot annotation number in project')
    skipped_annotations_number = serializers.IntegerField(default=None, read_only=True,
                                                      help_text='Skipped by collaborators annotation number in project')
    num_tasks_with_annotations = serializers.IntegerField(default=None, read_only=True, help_text='Tasks with annotations count')
    created_by = UserSimpleSerializer(default=CreatedByFromContext())

    parsed_label_config = SerializerMethodField(default=None, read_only=True,
                                                help_text='JSON-formatted labeling configuration')
    start_training_on_annotation_update = SerializerMethodField(default=None, read_only=False,
                                                                help_text='Start model training after any annotations are submitted or updated')
    config_has_control_tags = SerializerMethodField(default=None, read_only=True,
                                                    help_text='Flag to detect is project ready for labeling')

    @staticmethod
    def get_config_has_control_tags(project):
        return len(project.get_control_tags_from_config()) > 0

    @staticmethod
    def get_parsed_label_config(project):
        return project.get_parsed_config()

    def get_start_training_on_annotation_update(self, instance):
        # FIXME: remake this logic with start_training_on_annotation_update
        return True if instance.min_annotations_to_start_training else False

    def to_internal_value(self, data):
        # FIXME: remake this logic with start_training_on_annotation_update
        initial_data = data
        data = super().to_internal_value(data)
        if 'start_training_on_annotation_update' in initial_data:
            data['min_annotations_to_start_training'] = int(initial_data['start_training_on_annotation_update'])
        return data

    class Meta:
        model = Project
        extra_kwargs = {'memberships': {'required': False}, 'title': {'required': False}, 'created_by': {'required': False}}
        fields = ['id', 'title', 'description', 'label_config', 'expert_instruction', 'show_instruction', 'show_skip_button',
                  'enable_empty_annotation', 'show_annotation_history', 'organization', 'color',
                  'maximum_annotations', 'is_published', 'model_version', 'is_draft', 'created_by', 'created_at',
                  'min_annotations_to_start_training', 'start_training_on_annotation_update',
                  'show_collab_predictions', 'num_tasks_with_annotations',
                  'task_number', 'useful_annotation_number', 'ground_truth_number', 'skipped_annotations_number',
                  'total_annotations_number', 'total_predictions_number', 'sampling', 'show_ground_truth_first',
                  'show_overlap_first', 'overlap_cohort_percentage', 'task_data_login', 'task_data_password',
                  'control_weights', 'parsed_label_config', 'evaluate_predictions_automatically',
                  'config_has_control_tags', 'reveal_preannotations_interactively']

    def validate_label_config(self, value):
        if self.instance is None:
            # No project created yet
            Project.validate_label_config(value)
        else:
            # Existing project is updated
            self.instance.validate_config(value)
        return value


class ProjectOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectOnboarding
        fields = '__all__'


class ProjectLabelConfigSerializer(serializers.Serializer):
    label_config = serializers.CharField(help_text=Project.label_config.field.help_text)

    def validate_label_config(self, config):
        Project.validate_label_config(config)
        return config


class ProjectSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSummary
        fields = '__all__'


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = "__all__"


class FilterGroupSerializer(serializers.ModelSerializer):
    filters = FilterSerializer(many=True)

    class Meta:
        model = FilterGroup
        fields = "__all__"


class ViewSerializer(serializers.ModelSerializer):
    filter_group = FilterGroupSerializer(required=False)

    class Meta:
        model = View
        fields = "__all__"

    def to_internal_value(self, data):
        """
        map old filters structure to models
        "filters": {  ===> FilterGroup model
            "conjunction": "or",
            "items":[  ===> "filters" in FilterGroup
                 {  ==> Filter model
                   "filter":"filter:tasks:data.image", ==> column
                    "operator":"contains",
                    "type":"Image",
                    "value": <string: "XXX" | int: 123 | dict | list>
                 },
                  {
                    "filter":"filter:tasks:data.image",
                    "operator":"equal",
                    "type":"Image",
                    "value": <string: "XXX" | int: 123 | dict | list>
                 }
              ]
           }
        }
        """
        _data = data.get("data", {})

        filters = _data.pop("filters", {})
        conjunction = filters.get("conjunction")
        if "filter_group" not in data and conjunction:
            data["filter_group"] = {"conjunction": conjunction, "filters": []}
            if "items" in filters:
                for f in filters["items"]:
                    data["filter_group"]["filters"].append(
                        {
                            "column": f.get("filter", ""),
                            "operator": f.get("operator", ""),
                            "type": f.get("type", ""),
                            "value": f.get("value", {}),
                        }
                    )

        ordering = _data.pop("ordering", {})
        data["ordering"] = ordering

        return super().to_internal_value(data)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        filters = result.pop("filter_group", {})
        if filters:
            filters["items"] = []
            filters.pop("filters", [])
            filters.pop("id", None)

            for f in instance.filter_group.filters.order_by("index"):
                filters["items"].append(
                    {
                        "filter": f.column,
                        "operator": f.operator,
                        "type": f.type,
                        "value": f.value,
                    }
                )
            result["data"]["filters"] = filters

        selected_items = result.pop("selected_items", {})
        if selected_items:
            result["data"]["selectedItems"] = selected_items

        ordering = result.pop("ordering", {})
        if ordering:
            result["data"]["ordering"] = ordering
        return result

    @staticmethod
    def _create_filters(filter_group, filters_data):
        filter_index = 0
        for filter_data in filters_data:
            filter_data["index"] = filter_index
            filter_group.filters.add(Filter.objects.create(**filter_data))
            filter_index += 1

    def create(self, validated_data):
        with transaction.atomic():
            filter_group_data = validated_data.pop("filter_group", None)
            if filter_group_data:
                filters_data = filter_group_data.pop("filters", [])
                filter_group = FilterGroup.objects.create(**filter_group_data)

                self._create_filters(filter_group=filter_group, filters_data=filters_data)

                validated_data["filter_group_id"] = filter_group.id
            view = View.objects.create(**validated_data)

            return view

    def update(self, instance, validated_data):
        with transaction.atomic():
            filter_group_data = validated_data.pop("filter_group", None)
            if filter_group_data:
                filters_data = filter_group_data.pop("filters", [])

                filter_group = instance.filter_group
                if filter_group is None:
                    filter_group = FilterGroup.objects.create(**filter_group_data)

                conjunction = filter_group_data.get("conjunction")
                if conjunction and filter_group.conjunction != conjunction:
                    filter_group.conjunction = conjunction
                    filter_group.save()

                filter_group.filters.clear()
                self._create_filters(filter_group=filter_group, filters_data=filters_data)

            ordering = validated_data.pop("ordering", None)
            if ordering and ordering != instance.ordering:
                instance.ordering = ordering
                instance.save()

            if validated_data["data"] != instance.data:
                instance.data = validated_data["data"]
                instance.save()

            return instance


class DataManagerTaskSerializer(TaskSerializer):
    predictions = serializers.SerializerMethodField(required=False, read_only=True)
    annotations = serializers.SerializerMethodField(required=False, read_only=True)
    drafts = serializers.SerializerMethodField(required=False, read_only=True)
    annotators = serializers.SerializerMethodField(required=False, read_only=True)

    cancelled_annotations = serializers.IntegerField(required=False)
    total_annotations = serializers.IntegerField(required=False)
    total_predictions = serializers.IntegerField(required=False)
    completed_at = serializers.DateTimeField(required=False)
    annotations_results = serializers.SerializerMethodField(required=False)
    predictions_results = serializers.SerializerMethodField(required=False)
    predictions_score = serializers.FloatField(required=False)
    file_upload = serializers.SerializerMethodField(required=False)
    annotations_ids = serializers.SerializerMethodField(required=False)
    predictions_model_versions = serializers.SerializerMethodField(required=False)

    CHAR_LIMITS = 500

    class Meta:
        model = Task
        ref_name = 'data_manager_task_serializer'

        fields = [
            "cancelled_annotations",
            "completed_at",
            "created_at",
            "annotations_results",
            "data",
            "id",
            "predictions_results",
            "predictions_score",
            "total_annotations",
            "total_predictions",
            "annotations_ids",
            "annotations",
            "predictions",
            "drafts",
            "file_upload",
            "annotators",
            "project",
            'predictions_model_versions'
        ]

    def to_representation(self, obj):
        """ Dynamically manage including of some fields in the API result
        """
        ret = super(DataManagerTaskSerializer, self).to_representation(obj)
        if not self.context.get('annotations'):
            ret.pop('annotations', None)
        if not self.context.get('predictions'):
            ret.pop('predictions', None)
        return ret

    def _pretty_results(self, task, field, unique=False):
        if not hasattr(task, field) or getattr(task, field) is None:
            return ''

        result = getattr(task, field)
        if isinstance(result, str):
            output = result
            if unique:
                output = list(set(output.split(',')))
                output = ','.join(output)

        elif isinstance(result, int):
            output = str(result)
        else:
            result = [r for r in result if r is not None]
            if unique:
                result = list(set(result))
            result = round_floats(result)
            output = json.dumps(result, ensure_ascii=False)[1:-1]  # remove brackets [ ]

        return output[:self.CHAR_LIMITS].replace(',"', ', "').replace('],[', "] [").replace('"', '')

    def get_annotations_results(self, task):
        return self._pretty_results(task, 'annotations_results')

    def get_predictions_results(self, task):
        return self._pretty_results(task, 'predictions_results')

    def get_annotations(self, task):
        return AnnotationSerializer(task.annotations, many=True, default=[], read_only=True).data

    def get_predictions(self, task):
        return PredictionSerializer(task.predictions, many=True, default=[], read_only=True).data

    @staticmethod
    def get_file_upload(task):
        if not hasattr(task, 'file_upload_field'):
            return None
        file_upload = task.file_upload_field
        return os.path.basename(task.file_upload_field) if file_upload else None

    @staticmethod
    def get_annotators(obj):
        if not hasattr(obj, 'annotators'):
            return []

        annotators = obj.annotators
        if not annotators:
            return []
        if isinstance(annotators, str):
            annotators = [int(v) for v in annotators.split(',')]

        annotators = list(set(annotators))
        annotators = [a for a in annotators if a is not None]
        return annotators if hasattr(obj, 'annotators') and annotators else []

    def get_annotations_ids(self, task):
        return self._pretty_results(task, 'annotations_ids', unique=True)

    def get_predictions_model_versions(self, task):
        return self._pretty_results(task, 'predictions_model_versions', unique=True)

    def get_drafts(self, task):
        """Return drafts only for the current user"""
        # it's for swagger documentation
        if not isinstance(task, Task) or not self.context.get('drafts'):
            return []

        drafts = task.drafts
        if 'request' in self.context and hasattr(self.context['request'], 'user'):
            user = self.context['request'].user
            drafts = drafts.filter(user=user)

        return AnnotationDraftSerializer(drafts, many=True, read_only=True, default=True, context=self.context).data


class SelectedItemsSerializer(serializers.Serializer):
    all = serializers.BooleanField()
    included = serializers.ListField(child=serializers.IntegerField(), required=False)
    excluded = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate(self, data):
        if data["all"] is True and data.get("included"):
            raise serializers.ValidationError("included not allowed with all==true")
        if data["all"] is False and data.get("excluded"):
            raise serializers.ValidationError("excluded not allowed with all==false")

        view = self.context.get("view")
        request = self.context.get("request")
        if view and request and request.method in ("PATCH", "DELETE"):
            all_value = view.selected_items.get("all")
            if all_value and all_value != data["all"]:
                raise serializers.ValidationError("changing all value possible only with POST method")

        return data


class ViewResetSerializer(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

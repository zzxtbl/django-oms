# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import serializers
from workflow.models import ProcessCategory, Process, Node, Transition, ProcessInstance, Task, Event, Issue
from users.models import User
from django.core import serializers as ss
import json


class ProcessCategorySerializer(serializers.ModelSerializer):
    process = serializers.SerializerMethodField()

    class Meta:
        model = ProcessCategory
        fields = ('url', 'id', 'name', 'oid', 'is_active', 'process')

    def get_process(self, obj):
        data = Process.objects.filter(category=obj.id)
        return json.loads(ss.serialize('json', data))


class ProcessSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=ProcessCategory.objects.all(), slug_field='name')

    class Meta:
        model = Process
        fields = ('url', 'id', 'name', 'code', 'prefix', 'category', 'desc', 'oid', 'is_active', 'ext_data')


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('url', 'id', 'process', 'name', 'step', 'status', 'type', 'can_edit', 'can_reject', 'can_cancel',
                  'operators', 'desc', 'is_active', 'ext_data')


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = ('url', 'id', 'process', 'name', 'is_agree', 'can_auto_agree', 'routing_rule', 'input_node',
                  'output_node', 'desc', 'oid', 'is_active', 'ext_data')


class ProcessInstanceSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    cur_node = serializers.SlugRelatedField(queryset=Node.objects.all(), slug_field='name')

    class Meta:
        model = ProcessInstance
        fields = ('url', 'id', 'no', 'name', 'process', 'property', 'create_user', 'content_type', 'object_id',
                  'cur_node', 'create_time', 'start_time', 'end_time', 'desc')


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    agent_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Task
        fields = (
            'url', 'id', 'instance', 'node', 'user', 'agent_user', 'status', 'receive_time', 'is_hold', 'create_time')


class EventSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Event
        fields = (
            'url', 'id', 'instance', 'user', 'act_type', 'act_name', 'old_node', 'new_node', 'task', 'desc', 'ext_data',
            'create_time')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            'url', 'id', 'pinstance', 'name', 'summary', 'content', 'create_user', 'create_time')

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        issue.save()
        issue.create_pinstance('issue', True)
        return issue

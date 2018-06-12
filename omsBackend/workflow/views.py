# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from rest_framework.response import Response
from workflow.models import ProcessCategory, Process, Node, Transition, ProcessInstance, Task, Event, Issue
from workflow.serializers import (ProcessCategorySerializer, ProcessSerializer, NodeSerializer, TransitionSerializer,
                                  ProcessInstanceSerializer, TaskSerializer, EventSerializer, IssueSerializer)


class ProcessCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProcessCategory.objects.all()
    serializer_class = ProcessCategorySerializer


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class TransitionViewSet(viewsets.ModelViewSet):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer


class ProcessInstanceViewSet(viewsets.ModelViewSet):
    queryset = ProcessInstance.objects.all()
    serializer_class = ProcessInstanceSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

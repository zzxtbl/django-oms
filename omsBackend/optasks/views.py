# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from optasks.models import OpsProject, OpsDemandManager, OpsDemandEnclosure, ProjectComment
from optasks.serializers import (OpsProjectSerializer,
                                 OpsDemandManagerSerializer,
                                 OpsDemandEnclosureSerializer,
                                 ProjectCommentSerializer)
from optasks.filters import OpsProjectFilter


class OpsDemandManagerViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandManager.objects.all().order_by('start_time')
    serializer_class = OpsDemandManagerSerializer
    search_fields = ['name', 'pid']
    ordering_fields = ['task_complete', 'start_time', 'status']
    filter_fields = ['status', 'pid', 'create_user__username']


class OpsDemandEnclosureViewSet(viewsets.ModelViewSet):
    queryset = OpsDemandEnclosure.objects.all()
    serializer_class = OpsDemandEnclosureSerializer
    filter_fields = ['project__id']


class OpsProjectViewSet(viewsets.ModelViewSet):
    queryset = OpsProject.objects.all().order_by('-update_time', 'create_time')
    serializer_class = OpsProjectSerializer
    filter_class = OpsProjectFilter
    search_fields = ['pid', 'name', 'content1']


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectComment.objects.all().order_by('create_time')
    serializer_class = ProjectCommentSerializer
    filter_fields = ['project__id']
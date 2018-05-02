# -*- coding: utf-8 -*-
# author: itimor

from rest_framework import viewsets
from rest_framework.response import Response
from zbmanager.serializers import ZbHostSerializer, ZbHostGroupSerializer, ZbTemplateSerializer
from zbmanager.zabbix_api import ZabbixApi
from zbmanager.zabbix_conf import zabbix_info


class ZbHostViewSet(viewsets.ViewSet):
    serializer_class = ZbHostSerializer

    def list(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        limit = request.GET.get('limit', 10)
        offset = request.GET.get('offset', 0)
        query = zapi.get_hosts(limit=limit, offset=offset)
        serializer = ZbHostSerializer(query, many=True)
        return Response(serializer.data)


class ZbHostGroupViewSet(viewsets.ViewSet):
    serializer_class = ZbHostGroupSerializer

    def list(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        query = zapi.get_hostgroups()
        serializer = ZbHostGroupSerializer(query, many=True)
        return Response(serializer.data)


class ZbTemplateViewSet(viewsets.ViewSet):
    serializer_class = ZbTemplateSerializer

    def list(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        query = zapi.get_templetes()
        serializer = ZbTemplateSerializer(query, many=True)
        return Response(serializer.data)

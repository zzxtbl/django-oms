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
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        search = request.GET.get('search', None)
        query = zapi.get_hosts(search=search)
        serializer = ZbHostSerializer(query, many=True)
        data = dict()
        data['count'] = len(serializer.data)
        data['results'] = [serializer.data[i:i + limit] for i in range(0, len(serializer.data), limit)][offset]
        return Response(data)

    def post(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        if request.data['action'] == 'create':
            hostnames = request.data['hostnames']
            hostgroups = request.data['hostgroups']
            templates = request.data['templates']
            results = []
            for host in hostnames:
                hostName = host.split('|')[0]
                hostIp = host.split('|')[0]
                req = zapi.create_host(hostName, hostIp, hostgroups, templates)
                results.append(req)
            return Response(results)
        if request.data['action'] == 'update':
            hostId = request.data['hostId']
            hostName = request.data['hostName']
            hostIp = request.data['hostIp']
            hostgroups = request.data['hostgroups']
            templates = request.data['templates']
            results = zapi.update_host(hostId, hostName, hostIp, hostgroups, templates)
            return Response(results)
        if request.data['action'] == 'delete':
            hostIds = request.data['hostIds']
            results = zapi.delete_host(hostIds)
            return Response(results)


class ZbHostGroupViewSet(viewsets.ViewSet):
    serializer_class = ZbHostGroupSerializer

    def list(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        limit = request.GET.get('limit', 10)
        offset = request.GET.get('offset', 0)
        query = zapi.get_hostgroups()
        serializer = ZbHostGroupSerializer(query, many=True)
        data = dict()
        data['count'] = len(serializer.data)
        data['results'] = [serializer.data[i:i + int(limit)] for i in range(0, len(serializer.data), int(limit))][
            int(offset)]
        return Response(data)


class ZbTemplateViewSet(viewsets.ViewSet):
    serializer_class = ZbTemplateSerializer

    def list(self, request):
        zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
        zapi.login()
        query = zapi.get_templetes()
        serializer = ZbTemplateSerializer(query, many=True)
        return Response(serializer.data)

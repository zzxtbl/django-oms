# -*- coding: utf-8 -*-
# author: itimor
# docs: https://www.zabbix.com/documentation/3.4/zh/manual/api

import requests
import json


class ZabbixApi(object):
    def __init__(self, apiurl, username, password, auth_token=None):
        self.apiurl = apiurl
        self.username = username
        self.password = password
        self.header = {"Content-Type": "application/json"}
        self.auth_token = auth_token
        self.request_id = 1024

    def request(self, method, params):
        """
        Send request to Zabbix API
        :param method: Zabbix API 请求方法
        :param params: Zabbix API 请求参数
        :param auth_token: Zabbix API token
        :return: json
        """
        data = json.dumps({'jsonrpc': '2.0',
                           'method': method,
                           'params': params,
                           'auth': self.auth_token,
                           'id': self.request_id})
        req = requests.post(self.apiurl, data=data, headers=self.header)
        return json.loads(req.text)['result']

    def login(self):
        method = 'user.login'
        params = {
            'user': self.username,
            'password': self.password
        }
        req = self.request(method, params)
        self.auth_token = req

    def get_hosts(self, hostName=None):
        method = "host.get"
        params = {
            'output': 'extend',
            'filter': {'name': hostName}
        }
        req = self.request(method, params)
        return req

    def get_host_id(self, hostName):
        return self.get_hosts(hostName)[0]['hostid']

    def get_hostgroups(self, hostgroupName=None):
        method = "hostgroup.get"
        params = {
            'output': 'extend',
            'filter': {'name': hostgroupName}
        }
        req = self.request(method, params)
        return req

    def get_hostgroup_id(self, hostgroupName):
        return self.get_hostgroups(hostgroupName)[0]['groupid']

    def get_templetes(self, templateName=None):
        method = "template.get"
        params = {
            'output': 'extend',
            'filter': {'name': templateName}
        }
        req = self.request(method, params)
        return req

    def get_templete_id(self, templateName):
        return self.get_templetes(templateName)[0]['templateid']


if __name__ == '__main__':
    from zabbix_conf import zabbix_info

    zapi = ZabbixApi(zabbix_info['apiurl'], zabbix_info['username'], zabbix_info['password'])
    zapi.login()
    hosts = zapi.get_templete_id('Template OS Linux')
    print(hosts)

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
        data = json.dumps({"jsonrpc": "2.0",
                           "method": method,
                           "params": params,
                           "auth": self.auth_token,
                           "id": self.request_id})
        req = requests.post(self.apiurl, data=data, headers=self.header)
        return json.loads(req.text)["result"]

    def login(self):
        method = "user.login"
        params = {
            "user": self.username,
            "password": self.password
        }
        req = self.request(method, params)
        self.auth_token = req

    def get_hosts(self, add_params=None, limit=10, offset=0):
        method = "host.get"
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectInterfaces": "extend",
        }
        if add_params:
            params.update(add_params)
        req = self.request(method, params)
        data = dict()
        data['count'] = len(req)
        data['results'] = [req[i:i + int(limit)] for i in range(0, len(req), int(limit))][int(offset)]
        return data

    def get_hosts_byname(self, hostName):
        params = {"filter": {"name": hostName}}
        return self.get_hosts(params)

    def get_hosts_bygroup(self, groupids):
        params = {"groupids": groupids}
        return self.get_hosts(params)

    def get_hosts_byip(self, hostIp):
        params = {"filter": {"ip": hostIp}}
        return self.get_hosts(params)

    def get_hostgroups(self, add_params=None):
        method = "hostgroup.get"
        params = {
            "output": "extend",
            "selectHosts": "extend",
        }
        if add_params:
            params.update(add_params)
        req = self.request(method, params)
        return req

    def get_hostgroups_byname(self, hostgroupName):
        """
        :param hostgroupName: type list:
        :return:
        """
        params = {"filter": {"name": hostgroupName}}
        return self.get_hostgroups(params)

    def get_templetes(self, add_params=None):
        method = "template.get"
        params = {
            "output": "extend",
        }
        if add_params:
            params.update(add_params)
        req = self.request(method, params)
        return req

    def get_templetes_byname(self, templateName):
        params = {"filter": {"name": templateName}}
        return self.get_templetes(params)

    def create_host(self, hostName, hostIp, hostgroups=[], templates=[]):
        if self.get_hosts_byname(hostName) or self.get_hosts_byip(hostIp):
            return {"code": "10001", "msg": "The host was added, Please check later!"}

        group_list = [{"groupid": hostgroup_id} for hostgroup_id in hostgroups]
        template_list = [{"templateid": templete_id} for templete_id in templates]

        method = "host.create"
        params = {
            "host": hostName,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": hostIp,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": group_list,
            "templates": template_list,
        }
        req = self.request(method, params)
        return req

    def create_hostgroup(self, hostgroupName):
        if self.get_hostgroups_byname([hostgroupName]):
            return {"code": "10002", "msg": "The hostgroup was added, Please check later!"}

        method = "hostgroup.create"
        params = {"name": hostgroupName}
        req = self.request(method, params)
        return req

    def update_host(self, hostId, add_params=None):
        method = "host.update"
        params = {"hostid": hostId}
        if add_params:
            params.update(add_params)
        req = self.request(method, params)
        return req

    def delete_host(self, hosts):
        method = "host.delete"
        params = [host_id for host_id in hosts]
        req = self.request(method, params)
        return req


if __name__ == "__main__":
    from zabbix_conf import zabbix_info

    zapi = ZabbixApi(zabbix_info["apiurl"], zabbix_info["username"], zabbix_info["password"])
    zapi.login()
    groups = [
        "Zabbix servers",
        "Linux servers"
    ]
    hosts = zapi.get_hosts()
    print(hosts)

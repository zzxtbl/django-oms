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

    def get_hosts(self, hostName=None):
        method = "host.get"
        params = {
            "output": "extend",
            "filter": {"name": hostName}
        }
        req = self.request(method, params)
        return req

    def get_host_id(self, hostName):
        return self.get_hosts(hostName)[0]["hostid"]

    def get_hosts_byip(self, hostIp=None):
        method = "hostinterface.get"
        params = {
            "output": "extend",
            "filter": {"ip": hostIp}
        }
        req = self.request(method, params)
        return req

    def get_host_id_byip(self, hostIp):
        return self.get_hosts_byip(hostIp)[0]["hostid"]

    def get_hostgroups(self, hostgroupName=None):
        method = "hostgroup.get"
        params = {
            "output": "extend",
            "filter": {"name": hostgroupName}
        }
        req = self.request(method, params)
        return req

    def get_hostgroup_id(self, hostgroupName):
        return self.get_hostgroups(hostgroupName)[0]["groupid"]

    def get_templetes(self, templateName=None):
        method = "template.get"
        params = {
            "output": "extend",
            "filter": {"name": templateName}
        }
        req = self.request(method, params)
        return req

    def get_templete_id(self, templateName):
        return self.get_templetes(templateName)[0]["templateid"]

    def create_host(self, hostName, hostIp, hostgroups=[], templates=[]):
        if self.get_hosts(hostName) or self.get_hosts_byip(hostIp):
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
        if self.get_hostgroups(hostgroupName):
            return {"code": "10002", "msg": "The hostgroup was added, Please check later!"}

        method = "hostgroup.create"
        params = {"name": hostgroupName}
        req = self.request(method, params)
        return req

    def update_host(self, hostId, add_params):
        method = "host.update"
        params = {"hostid": hostId}
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
    hosts = zapi.get_hosts_byip("192.168.91.1")
    print(hosts)

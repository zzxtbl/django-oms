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
        self.request_id = 54088  # 意义非凡

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
        try:
            return json.loads(req.text)["result"]
        except:
            return json.loads(req.text)["error"]

    def login(self):
        method = "user.login"
        params = {
            "user": self.username,
            "password": self.password
        }
        req = self.request(method, params)
        self.auth_token = req

    def get_hosts(self, groupid=None, hostName=None, hostIp=None, search=None):
        method = "host.get"
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectInterfaces": "extend",
            "groupids": groupid,
            "filter": {
                "host": hostName,
                "ip": hostIp
            }
        }
        if search:
            params.update({"search": {
                "host": [search],
            }})
        req = self.request(method, params)
        return req

    def create_host(self, hostName, hostIp, hostgroups=[], templates=[]):
        if self.get_hosts(hostName=hostName) or self.get_hosts(hostIp=hostIp):
            return {"code": "10001", "message": "The host was added!"}

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
                    # "ip": hostIp,
                    "ip": "0.0.0.0",
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": group_list,
            "templates": template_list,
        }
        req = self.request(method, params)
        return req

    def update_host(self, hostId, hostName, hostIp, hostgroups=[], templates=[]):
        group_list = [{"groupid": hostgroup_id} for hostgroup_id in hostgroups]
        template_list = [{"templateid": templete_id} for templete_id in templates]

        method = "host.update"
        params = {
            "hostid": hostId,
            "host": hostName,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    # "ip": hostIp,
                    "ip": "0.0.0.0",
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": group_list,
            "templates": template_list,
        }
        req = self.request(method, params)
        return req

    def delete_host(self, hostIds=[]):
        method = "host.delete"
        params = hostIds
        req = self.request(method, params)
        return req

    def get_hostgroups(self, hostgroupName=None):
        method = "hostgroup.get"
        params = {
            "output": "extend",
            "selectHosts": "extend",
            "filter": {
                "name": hostgroupName
            }
        }
        req = self.request(method, params)
        return req

    def create_hostgroup(self, hostgroupName):
        if self.get_hostgroups([hostgroupName]):
            return {"code": "10002", "message": "The hostgroup was added!"}

        method = "hostgroup.create"
        params = {"name": hostgroupName}
        req = self.request(method, params)
        return req

    def get_templetes(self, templateName=None):
        method = "template.get"
        params = {
            "output": "extend",
            "filter": {
                "name": templateName
            }
        }
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
    #hosts = zapi.get_hosts()
    #hosts = zapi.get_templetes('Template SNMP OS Windows')
    #hosts = zapi.get_hostgroups('Virtual machines')
    h = {'hostids': ['10232']}
    hosts = zapi.create_host(['10232'])
    print(hosts)

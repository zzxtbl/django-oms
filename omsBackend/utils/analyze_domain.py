# -*- coding: utf-8 -*-
# author: itimor

import requests
import json
from datetime import datetime, timedelta
import logging
from bind_sendmail import SendMail

MAIL_ACOUNT = {
    "mail_host": "mail@oms.com",
    "mail_user": "admin@oms.com",
    "mail_pass": "jjyy",
    "mail_postfix": "oms.com",
}


def initlog(logfile):
    """
    创建日志实例
    """
    logger = logging.getLogger()
    hdlr = logging.FileHandler(logfile, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    return logger


def diffdns(alldomains, domainstatus_url, record_url):
    domains = json.loads(requests.get(alldomains).text)
    for domain in domains:
        urlinfos = json.loads(requests.get(domainstatus_url + domain).text)
        if not len(urlinfos):
            logging.error("%s - 收集的状态记录为空" % domain)
            continue

        ss = []
        ee = []
        for info in urlinfos:
            if info['status']:
                ss.append(info['node'])
            else:
                ee.append(info['node'])
        result = dict()
        result['node_count'] = len(urlinfos)
        result['error_node'] = ee
        result['url'] = domain

        if len(ss) > result['node_count'] / 2:
            result['status'] = True
            logging.info("%s - [域名正常，不需要变换ip] - %s" % (domain, result))
        else:
            result['status'] = False

            # 自动切换ip
            # x = domain.split('.')
            # domainname = '{}.{}'.format(x[1], x[2])
            # recordname = x[0]
            #
            # recorddata = json.loads(
            #     requests.get('{}?domain__name={}&name={}'.format(record_url, domainname, recordname)).text)[0]
            #
            # if recorddata['value2']:
            #     recorddata['value'], recorddata['value2'] = recorddata['value2'], recorddata['value']
            #     put_url = '{}{}/'.format(record_url, recorddata['id'])
            #     requests.put(put_url, data=recorddata)
            #     logging.warning("%s - [域名异常，ip已经自动更换] - %s" % (domain, result))
            # else:
            #     logging.error("%s - [域名异常，没有设置备用ip] - %s" % (domain, result))

            # 邮件通知
            sub = '%s 域名异常' % domain
            content = '大胸弟，%s 域名异常, 需要更换ip\n 详细信息：%s' % (domain, result)
            to_list = 'kiven@tb-gaming.com'
            cc_list = 'larry@tb-gaming.com'
            sendmail = SendMail(MAIL_ACOUNT, sub, content, to_list, cc_list)
            if sendmail.send_mail():
                logging.info("%s - [域名异常，通知邮件发送成功]" % domain)
            else:
                logging.error("%s - [域名异常，通知邮件发送失败]" % domain)

    logging.info("轮回结束，等待下一次...")
    return


if __name__ == '__main__':
    initlog('./tan.log')
    logging.info("命运的齿轮再次转动，轮回开始...")

    alldomains = 'http://118.193.136.206:8000/api/alldomains/'
    d = datetime.now()
    d10 = d - timedelta(minutes=10)
    cur_date = '{}-{}-{}'.format(d.year, d.month, d.day)
    cur_time = '{}:{}:{}'.format(d.hour, d.minute, d.second)
    create_time = '{}:{}:{}'.format(d10.hour, d10.minute, d10.second)
    # domainstatus_url = 'http://118.193.136.206:8000/api/domainstatus/?create_time_0={}&create_time_1={}&domain='.format(cur_date, create_time, cur_time)
    # record_url = 'http://oms.tb-gaming.local/api/dnsrecords/'
    domainstatus_url = 'http://118.193.136.206:8000/api/domainstatus/?domain='
    record_url = 'http://127.0.0.1:8000/api/dnsrecords/'
    print(diffdns(alldomains, domainstatus_url, record_url))

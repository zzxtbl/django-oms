/**
 * Created by Itimor on 2017/12/12.
 */

let CONFIG
const rest_url = 'oms.itimor.cf'
const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'

// if (process.env.NODE_ENV === 'development') {
if (process.env.NODE_ENV === 'production') {
  CONFIG = {
    apiUrl: '',
    zkapiUrl: 'http://172.19.6.99:9000',
    super_group: 'OMS_Super_Admin',
    wsurl: ws_scheme + '://' + rest_url + '/ws'
  }
} else if (process.env.NODE_ENV === 'test') {
  CONFIG = {
    apiUrl: 'http://oms.itimor.cf:8000',
    zkapiUrl: 'http://172.19.6.99:9000',
    super_group: 'admin',
    wsurl: ws_scheme + '://' + rest_url + '/ws'
  }
} else {
  CONFIG = {
    apiUrl: '',
    zkapiUrl: 'http://172.19.6.99:9000',
    super_group: 'admin',
    wsurl: ws_scheme + '://127.0.0.1:8000'
  }
}

/*
 接口API根地址
 */
const url = CONFIG.apiUrl
const zkurl = CONFIG.zkapiUrl

module.exports = {
  apiUrl: CONFIG.apiUrl,
  // 超级管理组
  super_group: CONFIG.super_group,

  // 表格数据
  LIMIT: 20,
  pagesize: [20, 50, 100],
  pageformat: 'total, prev, pager, next, sizes',

  // 本地上传到服务器
  uploadurl: `${url}/api/fileupload/`,
  // uploadurl: 'https://jsonplaceholder.typicode.com/posts/',

  // 登录
  login: `${url}/api/api-token-auth/`,
  // login: `${url}/api/api-auth/login/`,
  logout: `${url}/api/api-auth/logout/`,
  changePassword: `${url}/api/changepasswd/`,

  // 主机
  hosts: `${url}/api/hosts/`,
  idcs: `${url}/api/idcs/`,

  // 用户
  users: `${url}/api/users/`,
  groups: `${url}/api/groups/`,
  roles: `${url}/api/roles/`,

  // 工单
  worktickers: `${url}/api/worktickers/`,
  ticketcomments: `${url}/api/ticketcomments/`,
  ticketenclosures: `${url}/api/ticketenclosures/`,
  tickettypes: `${url}/api/tickettypes/`,
  records: `${url}/api/records/`,

  // 第三支付工单
  platforms: `${url}/api/platforms/`,
  merchants: `${url}/api/merchants/`,
  threepayenclosures: `${url}/api/threepayenclosures/`,
  paychannels: `${url}/api/paychannels/`,
  paychannelnames: `${url}/api/paychannelnames/`,
  threepaycomments: `${url}/api/threepaycomments/`,
  platformpaychannels: `${url}/api/platformpaychannels/`,

  // 权限
  usermenuperms: `${url}/api/usermenuperms/`,
  userhostperms: `${url}/api/userhostperms/`,
  userwikiperms: `${url}/api/userwikiperms/`,
  routerinfo: `${url}/api/routers/`,

  // 菜单
  firstmenus: `${url}/api/firstmenus/`,
  secondmenus: `${url}/api/secondmenus/`,
  menumetas: `${url}/api/menumetas/`,

  // tools
  uploads: `${url}/api/upload/`,
  sendmail: `${url}/api/sendmail/`,
  sendmessage: `${url}/api/sendmessage/`,
  calenders: `${url}/api/calenders/`,

  // 文档平台
  wikis: `${url}/api/wikis/`,
  opswikis: `${url}/api/opswikis/`,

  // 发布
  jobs: `${url}/api/jobs/`,
  deployenvs: `${url}/api/deployenvs/`,
  deployjobs: `${url}/api/deployjobs/`,
  deployresults: `${url}/api/deployresults/`,
  updaejobsstatus: `${url}/api/update_jobs_status/`,
  deploycmds: `${url}/api/deploycmds/`,
  deployversions: `${url}/api/deployversions/`,

  // 发布工单
  deploytickets: `${url}/api/deploytickets/`,
  deployticketenclosures: `${url}/api/deployticketenclosures/`,
  sqltickets: `${url}/api/sqltickets/`,

  // salt
  saltstates: `${url}/api/saltstates/`,
  saltstategroups: `${url}/api/saltstategroups/`,
  saltjobs: `${url}/api/saltjobs/`,
  cmdrun: `${url}/api/salts/cmdrun/`,
  get_cmd_result: `${url}/api/salts/get_cmd_result/`,
  update_states_status: `${url}/api/update_states_status/`,
  get_state_bygroup: `${url}/api/get_state_bygroup/`,
  sync_remote_server: `${url}/api/salts/sync_remote_server/`,

  // 项目
  projects: `${url}/api/projects/`,
  projectcompletes: `${url}/api/projectcompletes/`,
  projectcomments: `${url}/api/projectcomments/`,
  projectenclosures: `${url}/api/projectenclosures/`,
  projecttypes: `${url}/api/projecttypes/`,
  bugmanagers: `${url}/api/bugmanagers/`,
  testmanagers: `${url}/api/testmanagers/`,
  demandmanagers: `${url}/api/demandmanagers/`,
  demandenclosures: `${url}/api/demandenclosures/`,

  // 运维项目
  opsprojects: `${url}/api/opsprojects/`,
  opsdemandmanagers: `${url}/api/opsdemandmanagers/`,
  opsdemandenclosures: `${url}/api/opsdemandenclosures/`,
  opsprojectcomments: `${url}/api/opsprojectcomments/`,

  // zk考勤机
  zkusers: `${zkurl}/api/zkusers/`,
  zkpunchs: `${zkurl}/api/zkpunchs/`,
  zkpunchset: `${zkurl}/api/zkpunchset/`,

  // dnsapi
  dnsapikeys: `${url}/api/dnsapikeys/`,
  dnsdomains: `${url}/api/dnsdomains/`,
  dnsrecords: `${url}/api/dnsrecords/`,
  dnspoddomains: `${url}/api/dnspoddomains/`,
  dnspodrecords: `${url}/api/dnspodrecords/`,
  godaddydomains: `${url}/api/godaddydomains/`,
  godaddyreecords: `${url}/api/godaddyreecords/`,
  binddomains: `${url}/api/binddomains/`,
  bindrecords: `${url}/api/bindrecords/`,

  // zabbix
  zbhosts: `${url}/api/zbhosts/`,
  zbhostgroups: `${url}/api/zbhostgroups/`,
  zbtemplates: `${url}/api/zbtemplates/`
}

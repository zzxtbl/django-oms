import request from '@/utils/request'
import apiURL from '@/config'

// salts
export function getCmdrun(data) {
  return request({
    url: apiURL.cmdrun,
    method: 'post',
    data
  })
}

export function getSaltResult(jid) {
  return request({
    url: apiURL.get_cmd_result + jid,
    method: 'get'
  })
}

export function getSyncRemoteServer(method) {
  return request({
    url: apiURL.sync_remote_server + method,
    method: 'get'
  })
}

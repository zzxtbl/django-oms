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

// saltstates
export function postSaltState(data) {
  return request({
    url: apiURL.saltstates,
    method: 'post',
    data
  })
}

export function getSaltState(query, id) {
  return request({
    url: id ? apiURL.saltstates + id + '/' : apiURL.saltstates,
    method: 'get',
    params: query
  })
}

export function putSaltState(id, data) {
  return request({
    url: apiURL.saltstates + id + '/',
    method: 'put',
    data
  })
}

export function deleteSaltState(id) {
  return request({
    url: apiURL.saltstates + id + '/',
    method: 'delete'
  })
}

// saltstategroups
export function postSaltStateGroup(data) {
  return request({
    url: apiURL.saltstategroups,
    method: 'post',
    data
  })
}

export function getSaltStateGroup(query, id) {
  return request({
    url: id ? apiURL.saltstategroups + id + '/' : apiURL.saltstategroups,
    method: 'get',
    params: query
  })
}

export function putSaltStateGroup(id, data) {
  return request({
    url: apiURL.saltstategroups + id + '/',
    method: 'put',
    data
  })
}

export function deleteSaltStateGroup(id) {
  return request({
    url: apiURL.saltstategroups + id + '/',
    method: 'delete'
  })
}

// saltjobs
export function getSaltStateJob(query, id) {
  return request({
    url: id ? apiURL.saltjobs + id + '/' : apiURL.saltjobs,
    method: 'get',
    params: query
  })
}

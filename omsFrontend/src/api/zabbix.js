import request from '@/utils/request'
import apiUrl from '@/config'

// zbhosts
export function getzkHost(query) {
  return request({
    url: apiUrl.zbhosts,
    method: 'get',
    params: query
  })
}

export function postzkHost(data) {
  return request({
    url: apiUrl.zbhosts,
    method: 'post',
    data
  })
}

// zbhostgroups
export function getzkHostGroup(query) {
  return request({
    url: apiUrl.zbhostgroups,
    method: 'get',
    params: query
  })
}

// zbtemplates
export function getzkTemplate(query) {
  return request({
    url: apiUrl.zbtemplates,
    method: 'get',
    params: query
  })
}

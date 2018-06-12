import request from '@/utils/request'
import apiUrl from '@/config'

// users
export function postUser(data) {
  return request({
    url: apiUrl.users,
    method: 'post',
    data
  })
}

export function getUser(query) {
  return request({
    url: apiUrl.users,
    method: 'get',
    params: query
  })
}

export function patchUser(id, data) {
  return request({
    url: apiUrl.users + id + '/',
    method: 'patch',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: apiUrl.users + id + '/',
    method: 'delete'
  })
}

// groups
export function postGroup(data) {
  return request({
    url: apiUrl.groups,
    method: 'post',
    data
  })
}

export function getGroup(query) {
  return request({
    url: apiUrl.groups,
    method: 'get',
    params: query
  })
}

export function putGroup(id, data) {
  return request({
    url: apiUrl.groups + id + '/',
    method: 'put',
    data
  })
}

export function deleteGroup(id) {
  return request({
    url: apiUrl.groups + id + '/',
    method: 'delete'
  })
}

// roles
export function postRole(data) {
  return request({
    url: apiUrl.roles,
    method: 'post',
    data
  })
}

export function getRole(query) {
  return request({
    url: apiUrl.roles,
    method: 'get',
    params: query
  })
}

export function putRole(id, data) {
  return request({
    url: apiUrl.roles + id + '/',
    method: 'put',
    data
  })
}

export function deleteRole(id) {
  return request({
    url: apiUrl.roles + id + '/',
    method: 'delete'
  })
}

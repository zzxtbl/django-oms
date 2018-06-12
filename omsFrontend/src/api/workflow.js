import request from '@/utils/request'
import apiUrl from '@/config'

// wfcategorys
export function postWfcategory(data) {
  return request({
    url: apiUrl.wfcategorys,
    method: 'post',
    data
  })
}

export function getWfcategory(query) {
  return request({
    url: apiUrl.wfcategorys,
    method: 'get',
    params: query
  })
}

export function putWfcategory(id, data) {
  return request({
    url: apiUrl.wfcategorys + id + '/',
    method: 'put',
    data
  })
}

export function deleteWfcategory(id) {
  return request({
    url: apiUrl.wfcategorys + id + '/',
    method: 'delete'
  })
}

// wfinstances
export function postWfinstance(data) {
  return request({
    url: apiUrl.wfinstances,
    method: 'post',
    data
  })
}

export function getWfinstance(query) {
  return request({
    url: apiUrl.wfinstances,
    method: 'get',
    params: query
  })
}

export function putWfinstance(id, data) {
  return request({
    url: apiUrl.wfinstances + id + '/',
    method: 'put',
    data
  })
}

export function deleteWfinstance(id) {
  return request({
    url: apiUrl.wfinstances + id + '/',
    method: 'delete'
  })
}

// wftasks
export function postWftask(data) {
  return request({
    url: apiUrl.wftasks,
    method: 'post',
    data
  })
}

export function getWftask(query) {
  return request({
    url: apiUrl.wftasks,
    method: 'get',
    params: query
  })
}

export function putWftask(id, data) {
  return request({
    url: apiUrl.wftasks + id + '/',
    method: 'put',
    data
  })
}

export function deleteWftask(id) {
  return request({
    url: apiUrl.wftasks + id + '/',
    method: 'delete'
  })
}

// wfevents
export function postWfevent(data) {
  return request({
    url: apiUrl.wfevents,
    method: 'post',
    data
  })
}

export function getWfevent(query) {
  return request({
    url: apiUrl.wfevents,
    method: 'get',
    params: query
  })
}

export function putWfevent(id, data) {
  return request({
    url: apiUrl.wfevents + id + '/',
    method: 'put',
    data
  })
}

export function deleteWfevent(id) {
  return request({
    url: apiUrl.wfevents + id + '/',
    method: 'delete'
  })
}

// wfissues
export function postWfissue(data) {
  return request({
    url: apiUrl.wfissues,
    method: 'post',
    data
  })
}

export function getWfissue(query) {
  return request({
    url: apiUrl.wfissues,
    method: 'get',
    params: query
  })
}

export function putWfissue(id, data) {
  return request({
    url: apiUrl.wfissues + id + '/',
    method: 'put',
    data
  })
}

export function deleteWfissue(id) {
  return request({
    url: apiUrl.wfissues + id + '/',
    method: 'delete'
  })
}

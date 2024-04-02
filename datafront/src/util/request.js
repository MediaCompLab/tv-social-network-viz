import axios from 'axios'
import qs from 'qs'
import router from '@/router';
import { getToken } from '@/util/auth'
import {
    ElMessage
} from 'element-plus'
// create an axios instance
const service = axios.create({
  baseURL: 'http://127.0.0.1:5000', 
  timeout: 50000, // request timeout
  headers: {
    'Content-Type': 'application/json; charset=utf-8'
    // 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
})

service.interceptors.request.use(
  config => {
    if (getToken()) {
      config.headers['Authorization'] = getToken()
    } 
    return config
  },
  error => {
    return Promise.error(error)
  }
)

/**
 * 响应拦截器
 * 统一处理失败情况，并将失败信息弹窗显示
 */
service.interceptors.response.use(
  response => {
    if (response.data.code === 401) {
      ElMessage.warning(response.data.msg)
      router.replace('/login')

    } else if (response.status === 200) {
      return Promise.resolve(response)
    } else {
      ElMessage.warning('接口调用异常')
      return Promise.reject(response);
    }
  },
  error => {
    ElMessage.warning('接口调用超时')
    console.log('error response:',error)
  }
)

/** 统一的get请求 */
export function get(url, params) {
    return new Promise((resolve, reject) => {
      service({
        url: url,
        method: 'get',
        params: params
      }).then(res => {
        resolve(res.data)
      }).catch(err => {
        reject(err.data)
      })
    })
  }
  
  /** 统一的post请求 */
  export function post(url, params, headers) {
    if (headers == null) {
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
      }
    }
    return new Promise((resolve, reject) => {
      service({
        url: url,
        method: 'post',
        // data: qs.stringify(params),
        data: params,
        headers: headers
      }).then(res => {
        resolve(res.data)
      }).catch(err => {
        reject(err.data)
      })
    })
  }
  
  /** 统一put请求 */
  export function put(url, params, headers) {
    if (headers == null) {
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
      }
    }
    return new Promise((resolve, reject) => {
      service({
        url: url,
        method: 'put',
        data: qs.stringify(params),
        headers: headers
      }).then(res => {
        resolve(res.data)
      }).catch(err => {
        reject(err.data)
      })
    })
  }
  
  
  /** 统一put请求 */
  export function del(url, params, headers) {
    if (headers == null) {
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
      }
    }
    return new Promise((resolve, reject) => {
      service({
        url: url,
        method: 'delete',
        data: qs.stringify(params),
        headers: headers
      }).then(res => {
        resolve(res.data)
      }).catch(err => {
        reject(err.data)
      })
    })
  }
  
  
  export function upload(url, params, headers) {
    if (headers == null) {
      headers = {
        "Content-Type": "multipart/form-data",
      }
    }
    return new Promise((resolve, reject) => {
      service({
        url: url,
        method: 'post',
        data: params,
        headers: headers
      }).then(res => {
        resolve(res.data)
      }).catch(err => {
        reject(err.data)
      })
    })
  }
  
  
  
export default {
    service
  }
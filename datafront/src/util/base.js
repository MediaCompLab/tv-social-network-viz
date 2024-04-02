const base={
    //登录
     login:"/login",
     register:'/register',
     uploadfiles:'/uploadfiles',
     mergefile:'/mergefile',
     apifirstnode:'/apifirstnode',
     apisecnode:'/apisecnode',
     apithrnode:'/apithrnode',
     apifounode:'/apifounode',
     apifivnode:'/apifivnode',
     apidraw:'/apidraw',
     apiverify:'/apiverify',
     apiunibatchno:'/apiunibatchno',
     apidelnode:'/apidelnode'
}
import {get,post,put,del,upload} from "@/util/request"
export function login(params){
    return post(base.login,params)
}

export function register(params){
    return post(base.register,params)
}

export function upfiles(params){
    return upload(base.uploadfiles,params)
}

export function mergefile(params){
    return get(base.mergefile,params)
}

export function getfirData(params){
    return get(base.apifirstnode,params)
}
export function getsecData(params){
    return post(base.apisecnode,params)
}
export function getthrData(params){
    return post(base.apithrnode,params)
}
export function getfouData(params){
    return post(base.apifounode,params)
}
export function getfivData(params){
    return post(base.apifivnode,params)
}
export function darwgeo(params){
    return post(base.apidraw,params)
}

export function apiverify(params){
    return get(base.apiverify,params)
}

export function unibno(params){
    return post(base.apiunibatchno,params)
}
export function delnode(params){
    return post(base.apidelnode,params)
}
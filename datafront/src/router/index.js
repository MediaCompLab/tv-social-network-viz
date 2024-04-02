import { createRouter,createWebHashHistory } from "vue-router";
import {getToken} from '@/util/auth.js'

// import Login from '@/views/login/index.vue'
// import About from '../views/About.vue'
// import List from '../views/List.vue'
// import Detail from '../views/Detail.vue'
const routes = [
    {
        path: "/login", // 默认路由 home页面
        component: () => import("@/views/login/index.vue"),
      },
      {
        path: "/register", // 默认路由 home页面
        component: () => import("@/views/register/index.vue"),
      },
      {
        path: "/", // 默认路由 home页面
        component: () => import("@/views/layout/index.vue"),
        redirect:'/draw',
        children: [{
          path: 'dashboard',
          name: 'Dashboard',
          component: () => import('@/views/dashboard/index.vue'),
          meta: { title: 'Dashboard', icon: 'el-icon-s-home'}
        },
        {
          path: 'tranfile',
          name: 'tranfile',
          component: () => import('@/views/sys/tranfile.vue'),
          meta: { title: 'tranfile', icon: 'el-icon-s-home',keepAlive: true }
        },
        {
          path: 'draw',
          name: 'draw',
          component: () => import('@/views/sys/draw.vue'),
          meta: { title: 'draw', icon: 'el-icon-s-home'}
        }
      ]
      },
  ]

  const router = createRouter({
    history:createWebHashHistory(),
    routes
  })
  router.beforeEach((to, from, next) => {
    if(to.fullPath==='/register' || to.fullPath==='/login'||getToken()){
      next()
    }
    else{
      next('/login')
    }
})

  export default router
    
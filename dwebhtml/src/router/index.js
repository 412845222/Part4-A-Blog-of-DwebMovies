import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from '../store'
Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: (to, from, next) => {
      if (store.state.userinfo.token) {
        next()
      }else{
        next('/login')
      }
    }
  },
  //登录
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../views/Login.vue')
  },
  //注册
  {
    path: '/register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "about" */ '../views/Register.vue')
  },
  //发布文章
  {
    path: '/add-article',
    name: 'AddArticle',
    component: () => import(/* webpackChunkName: "about" */ '../views/AddArticle.vue'),
    beforeEnter: (to, from, next) => {
      if (store.state.userinfo.token) {
        next()
      }else{
        next('/login')
      }
    }
  },
  //文章列表
  {
    path: '/article-list',
    name: 'ArticleList',
    component: () => import(/* webpackChunkName: "about" */ '../views/ArticleList.vue'),
    beforeEnter: (to, from, next) => {
      if (store.state.userinfo.token) {
        next()
      }else{
        next('/login')
      }
    }
  },
  //用户管理
  {
    path: '/user-permission',
    name: 'UserPerm',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserPerm.vue'),
    beforeEnter: (to, from, next) => {
      //判断用户登录
      if (store.state.userinfo.token) {
        //判断用户权限
        // let checkInfo = {
        //   contentType:'auth_user',
        //   permissions:['add','change','delete','view']
        // }
        // store.dispatch("checkUserPerm",checkInfo)
        next()
      }else{
        next('/login')
      }
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const routerPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return routerPush.call(this,location).catch(err=>err)
}



const router = new VueRouter({
  routes
})

//全局路由
// router.beforeEach((to,from,next)=>{
//   console.log(to.path)
//   console.log(from.path)
//   next()
// })



export default router

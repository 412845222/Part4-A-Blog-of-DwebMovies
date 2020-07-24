import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userinfo:{}
  },
  mutations: {
    //保存 注册登录用户信息
    saveUserinfo(state,userinfo){
      state.userinfo = userinfo
    }
  },
  actions: {
  },
  modules: {
  }
})

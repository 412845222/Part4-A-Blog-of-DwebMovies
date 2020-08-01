import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import Qs from "qs";
import router from "../router"
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userinfo: {},
  },
  getters:{
    //查询登录状态
    isnotUserlogin(state){
      return state.userinfo.token
    }
  },
  mutations: {
    //保存 注册登录用户信息
    saveUserinfo(state, userinfo) {
      state.userinfo = userinfo;
    },
    //清空 用户登录状态
    clearUserinfo(state){
      state.userinfo = {}
    }
  },
  actions: {
    //登录
    blogLogin({ commit }, formData) {
      axios({
        url: "http://127.0.0.1:9000/api/dweb-login/",
        method: "post",
        data: Qs.stringify(formData),
      }).then((res) => {
        if (res.data == "none") {
          alert("用户名不存在");
          return;
        }
        if (res.data == "pwderr") {
          alert("密码错误");
          return;
        }
        console.log(res.data);
        commit("saveUserinfo", res.data);
        //缓存
        localStorage.setItem('token',res.data.token)
        router.push({path:'/'})
      });
    },
    //注册
    blogRegister({ commit }, formData) {
      axios({
        url: "http://127.0.0.1:9000/api/dweb-register/",
        method: "post",
        data: Qs.stringify(formData),
      }).then((res) => {
        if (res.data == "repeat") {
          alert("用户名已存在");
          return;
        }
        console.log(res.data);
        commit("saveUserinfo", res.data);
        //缓存
        localStorage.setItem('token',res.data.token)
        router.push({path:'/'})
      });
    },
    //自动登录
    tryAutoLogin({commit}){
      let token = localStorage.getItem('token')
      if (token) {
        axios({
          url:"http://127.0.0.1:9000/api/auto-login/",
          method:"post",
          data:Qs.stringify({token})
        }).then((res)=>{
          console.log(res.data)
          if (res.data == 'tokenTimeout') {
            alert('用户信息过期，重新登录')
            return
          }
          commit("saveUserinfo", res.data);
          //缓存
          localStorage.setItem('token',res.data.token)
          router.push({path:'/'})
        })
      }
    },
    //登出
    blogLogout({commit},token){
      commit('clearUserinfo')
      localStorage.removeItem('token')
      // router.push({path:'/'})
      axios({
        url:"http://127.0.0.1:9000/api/dweb-logout/",
        method:'post',
        data:Qs.stringify({token})
      }).then((res)=>{
        console.log(res.data)
      })
    }
  },
  modules: {},
});

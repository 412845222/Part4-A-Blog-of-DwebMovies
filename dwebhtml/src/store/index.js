import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import Qs from "qs";
import router from "../router"
import swal from "sweetalert"
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
        url: "https://api.study.dweb.club/api/dweb-login/",
        method: "post",
        data: Qs.stringify(formData),
      }).then((res) => {
        if (res.data == "none") {
          swal('错误','用户名不存在','error')
          return;
        }
        if (res.data == "pwderr") {
          swal('错误','密码错误','error')
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
        url: "https://api.study.dweb.club/api/dweb-register/",
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
          url:"https://api.study.dweb.club/api/auto-login/",
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
        url:"https://api.study.dweb.club/api/dweb-logout/",
        method:'post',
        data:Qs.stringify({token})
      }).then((res)=>{
        console.log(res.data)
      })
    },
    //权限判断
    async checkUserPerm({getters},checkInfo){
      //用户
      let token = getters.isnotUserlogin
      //表
      let contentType = checkInfo.contentType
      //权限
      let permissions = checkInfo.permissions
      //鉴权结果
      let perm_data;
      await axios({
        url:"https://api.study.dweb.club/api/dweb-checkperm/",
        method:'post',
        data:Qs.stringify({
          token,
          contentType,
          permissions:JSON.stringify(permissions)
        })
      }).then((res)=>{
        // console.log(res.data)
        if (res.data == 'nologin') {
          perm_data = false
          alert('用户信息错误')
          return
        }
        if (res.data == 'noperm') {
          perm_data = false
          alert('用户权限不足，联系管理员')
          return
        }
        if (res.data == "ok") {
          perm_data = true
        }
      })
      return perm_data
    }
  },
  modules: {},
});

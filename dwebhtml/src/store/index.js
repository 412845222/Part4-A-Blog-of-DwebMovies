import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import Qs from "qs";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userinfo: {},
  },
  getters:{
    
  },
  mutations: {
    //保存 注册登录用户信息
    saveUserinfo(state, userinfo) {
      state.userinfo = userinfo;
    },
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
      });
    },
  },
  modules: {},
});

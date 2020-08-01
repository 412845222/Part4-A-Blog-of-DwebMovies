<template>
  <div id="app">
    <!-- 头部导航 -->
    <div id="top-menu" class="dweb"></div>
    <!-- 侧边栏 左 导航 -->
    <div id="left-menu" :class="'dweb ' + mobile_left">
      <i @click="showHideLeftMenu" id="left-btn" class="el-icon-menu"></i>
      <!-- 导航栏 -->
      <el-col :span="24" style="margin-top:80px">
        <el-menu
          class="el-menu-vertical-demo"
          background-color="#00000000"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="chooseMenu"
        >
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-folder-opened"></i>
              <span>文章管理</span>
            </template>
            <el-menu-item-group>
              <el-menu-item  index="/add-article">发布文章</el-menu-item>
              <el-menu-item index="1-2">文章列表</el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-menu-item index="2">
            <i class="el-icon-user"></i>
            <span slot="title">用户管理</span>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-money"></i>
            <span slot="title">打赏记录</span>
          </el-menu-item>
          <el-menu-item index="5">
            <i class="el-icon-s-operation"></i>
            <span slot="title">栏目管理</span>
          </el-menu-item>
          <el-menu-item v-if="authUserLogin" @click="blogLogout()">
            <i class="el-icon-back"></i>
            <span slot="title">退出登录</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </div>
    <!-- 页面内容 -->
    <div id="content" :class="moblie_content">
      <router-view></router-view>

      <div id="footer" class="dweb">
        <span>Copyright © 2020 Dweb工作室</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      screenWidth: document.body.clientWidth,
      mobile_left: "",
      moblie_content: "",
    };
  },
  computed: {
    //验证用户是否登录
    authUserLogin(){
      return this.$store.getters.isnotUserlogin
    }
  },
  watch: {
    //监听用户token
    authUserLogin(newVal){ 
      if (newVal==null) {
        this.$router.push({path:'/login'})
      }
    }
  },
  created() {
    this.$store.dispatch('tryAutoLogin')
  },
  mounted() {
    this.changeDevice();
  },
  methods: {
    chooseMenu(index) {
      // console.log(index);
      this.$router.push({ path: index });
    },
    changeDevice() {
      if (this.screenWidth <= 500) {
        this.mobile_left = "xs";
        this.moblie_content = "xs";
      }
    },
    showHideLeftMenu() {
      if (this.mobile_left == "") {
        this.mobile_left = "xs";
      } else {
        this.mobile_left = "";
      }
      //宽屏
      if (this.screenWidth > 500) {
        if (this.moblie_content == "") {
          this.moblie_content = "xs";
        } else {
          this.moblie_content = "";
        }
      }
    },
    //退出登录
    blogLogout(){
      this.$store.dispatch('blogLogout',this.$store.getters.isnotUserlogin)
    }
  },
};
</script>

<style>
.el-col {
  margin-top: 5px;
}
</style>

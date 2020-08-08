<template>
  <div>
    <!-- 面包屑导航 -->
    <div class="dweb">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="body dweb">
      <div class="dweb">
        <h5>用户组</h5>
        <el-divider></el-divider>
      </div>
    </div>
  </div>
</template>

<script>
import store from "../store";
export default {
  beforeRouteEnter(to, from, next) {
    //判断用户权限
    let checkInfo = {
      contentType: "auth_user",
      permissions: ["add", "change", "delete", "view"],
    };
    store.dispatch("checkUserPerm", checkInfo);
    next()
  },
};
</script>

<style scoped>
.dweb {
  padding: 10px 10px;
}
</style>

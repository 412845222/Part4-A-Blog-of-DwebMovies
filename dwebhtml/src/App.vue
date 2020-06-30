<template>
  <div id="app">
    <!-- 头部导航 -->
    <div id="top-menu" class="dweb"></div>
    <!-- 侧边栏 左 导航 -->
    <div id="left-menu" class="dweb"></div>
    <!-- 页面内容 -->
    <div id="content" class="">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
        <el-col :span="8">
          <div class="dweb" style="height:250px"></div>
        </el-col>
      </el-row>

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
      value: true,
    };
  },
};
</script>

<style>
.el-col {
  margin-top: 5px;
}
</style>

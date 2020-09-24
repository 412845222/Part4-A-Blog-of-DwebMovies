<template>
  <div id="article-list">
    <!-- 面包屑导航 -->
    <div class="dweb">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>文章列表</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 文章列表 -->
    <div class="dweb" style="margin-top:10px">
      <el-row>
        <el-col v-for="item in article_list" :key="item.id" :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="item.cover"
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="item.cover"
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span>{{ item.title }}</span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span> 发布者：{{ item.nickName }} </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  @click="toArticle(item.id)"
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  @click="deleteArticle(item.id)"
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 分页器 -->
    <div class="dweb" style="margin-top:10px">
      <el-pagination
        background
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        @current-change="currentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
import swal from "sweetalert";
export default {
  props: ["screenWidth"],
  data() {
    return {
      currentPage: 1,
      pageSize: 5,
      total: 100,
      article_list: [],
    };
  },
  mounted() {
    this.getListData(this.currentPage);
  },
  methods: {
    //跳转内容页
    toArticle(id) {
      console.log("开始跳转");
      this.$router.push({ path: "/article", query: { id: id } });
    },
    getListData(page) {
      axios({
        url: "https://api.study.dweb.club/api/article-list/",
        method: "get",
        params: {
          page,
          pageSize: this.pageSize,
          lanmu: "all",
        },
      }).then((res) => {
        console.log(res.data);
        this.article_list = res.data.data;
        this.total = res.data.total;
      });
    },
    currentChange(val) {
      console.log("第" + val + "页");
      this.currentPage = val;
      this.getListData(val);
    },
    //删除文章
    deleteArticle(id) {
      swal({
        title: "删除提醒",
        text: "是否确定删除",
        icon: "warning",
        buttons: true,
      }).then((willDelete) => {
        if (willDelete) {
          let checkInfo = {
            contentType: "blog_article",
            permissions: ["delete"],
          };
          this.$store.dispatch("checkUserPerm", checkInfo).then((res) => {
            console.log(res);
            if (res) {
              axios({
                url: "https://api.study.dweb.club/api/delete-article/",
                method: "delete",
                data: Qs.stringify({
                  id,
                  token: this.$store.getters.isnotUserlogin,
                }),
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
              }).then((res) => {
                console.log(res);
                if (res.data == "nologin") {
                  alert("用户登录信息错误");
                  return;
                }
                if (res.data == "noperm") {
                  alert("权限不足");
                }
                this.getListData(this.currentPage);
              });
            }
          });
        }
      });
      // if (confirm("是否确定删除")) {
      // }
    },
  },
};
</script>

<style scoped>
#article-list .dweb {
  padding: 10px 10px;
}
.card.dweb .text-item {
  color: #fff;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

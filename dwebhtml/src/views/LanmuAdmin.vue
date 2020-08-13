<template>
  <div>
    <!-- 面包屑导航 -->
    <BreadMenu :page_name="'栏目管理'"></BreadMenu>

    <!-- 内容 -->
    <div class="body dweb">
      <el-row :gutter="10">
        <el-col :span="6">
          <div class="dweb">
            <h5>栏目结构</h5>
            <el-divider></el-divider>
          </div>
          <div class="body dweb" style="display:flex">
            <el-input
              v-model="new_lanmu_name"
              placeholder="请输入新栏目名称"
            ></el-input>
            <el-button @click="pushLanmuList()" type="success">保存</el-button>
          </div>
          <div class="body dweb">
            <el-tree
              :data="lanmu_tree"
              node-key="id"
              default-expand-all
              draggable
              :render-content="renderContent"
              @node-click="choosed_lanmu_articleList"
            >
            </el-tree>
          </div>

          <div class="save-tree body dweb" style="float:left;">
            <el-button @click="getLanmuTree()" type="warning" size="mini"
              >恢复结构</el-button
            >
            <el-button @click="saveLanmuTree()" type="success" size="mini"
              >保存结构</el-button
            >
            <el-button
              @click="getListData(1, 'nobelong')"
              type="primary"
              size="mini"
              >未分配文章获取</el-button
            >
          </div>
        </el-col>

        <el-col :span="18">
          <div class="dweb">
            <h5>文章列表</h5>
            <el-divider></el-divider>
          </div>

          <!-- 文章列表 -->
          <div class="dweb" style="margin-top:10px;min-height:468px">
            <el-row>
              <el-col v-for="item in article_list" :key="item.id" :span="24">
                <div class="card dweb">
                  <el-row>
                    <el-col :xs="24" :lg="6">
                      <el-image
                        style="height:60px"
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
                      <el-popover placement="right" width="80" trigger="click">
                        <el-tree
                          :data="lanmu_tree"
                          node-key="id"
                          default-expand-all
                          @node-click="choosed_lanmu"
                        >
                        </el-tree>
                        <el-button
                          type="warning"
                          icon="el-icon-plus"
                          circle
                          slot="reference"
                        ></el-button>
                        <el-button
                          type="success"
                          size="mini"
                          @click="saveArticleToLanmu(item.id)"
                        >
                          确定</el-button
                        >
                      </el-popover>
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
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import BreadMenu from "../components/BreadMenu";
import axios from "axios";
import Qs from "qs";
export default {
  data() {
    return {
      //文章内容+
      currentPage: 1,
      currentLanmu: "nobelong",
      pageSize: 4,
      total: 100,
      article_list: [],
      //栏目结构
      maxId: 0,
      new_lanmu_name: "",
      lanmu_tree: [],
      //文章栏目分配、
      choosed_lanmu_id: 0,
      choosed_article_id: 0,
    };
  },
  components: {
    BreadMenu,
  },
  mounted() {
    this.getListData(this.currentPage, this.currentLanmu);
    this.getLanmuTree();
  },
  methods: {
    //选择栏目查看文章
    choosed_lanmu_articleList(node) {
      let lanmu_name = node.label;
      this.getListData(1, lanmu_name);
    },
    //选择文章保存栏目
    choosed_lanmu(node) {
      console.log(node);
      this.choosed_lanmu_id = node.id;
      this.choosed_lanmu_name = node.label
    },
    saveArticleToLanmu(article_id) {
      axios({
        url: "http://127.0.0.1:9000/api/add-article/",
        method: "put",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserlogin,
          lanmu_id: this.choosed_lanmu_id,
          article_id: article_id,
        }),
      }).then((res) => {
        if (res.data == "nologin") {
          alert("尚未登录");
          return;
        }
        if (res.data == "noperm") {
          alert("权限不足");
          return;
        }
        if (res.data == "ok") {
          console.log(res.data);
          this.getListData(1, this.choosed_lanmu_name);
          this.getLanmuTree();
        }
      });
    },
    //获取栏目数据
    getLanmuTree() {
      axios({
        url: "http://127.0.0.1:9000/api/dweb-lanmu/",
        method: "get",
      }).then((res) => {
        console.log(res.data);
        this.lanmu_tree = res.data;
      });
    },
    //保存栏目结构
    saveLanmuTree() {
      console.log(this.lanmu_tree);
      axios({
        url: "http://127.0.0.1:9000/api/dweb-lanmu/",
        method: "put",
        data: Qs.stringify({
          token: this.$store.getters.isnotUserlogin,
          lanmu_tree: JSON.stringify(this.lanmu_tree),
        }),
      }).then((res) => {
        console.log(res.data);
        if (res.data == "nologin") {
          alert("尚未登录");
          return;
        }
        if (res.data == "noperm") {
          alert("权限不足");
          return;
        }
      });
    },
    //新栏目名称
    pushLanmuList() {
      let checkTree = this.loopCheckData(this.lanmu_tree);
      console.log(checkTree);
      if (checkTree == false) {
        this.new_lanmu_name = "";
        return;
      }
      let new_lanmu = {
        id: this.maxId + 1,
        label: this.new_lanmu_name,
        children: [],
      };
      console.log(new_lanmu);

      this.lanmu_tree.push(new_lanmu);
      this.new_lanmu_name = "";
    },
    loopCheckData(tree) {
      let checkTree = true;
      //检查新栏目数据
      tree.forEach((obj) => {
        if (obj.id > this.maxId) {
          this.maxId = obj.id;
        }
        if (obj.label == this.new_lanmu_name) {
          alert("命名重复");
          checkTree = false;
          return;
        }
        if (obj.children) {
          if (obj.children.length > 0) {
            this.loopCheckData(obj.children);
          }
        }
      });

      return checkTree;
    },
    getListData(page, lanmu) {
      axios({
        url: "http://127.0.0.1:9000/api/article-list/",
        method: "get",
        params: {
          page,
          pageSize: this.pageSize,
          lanmu: lanmu,
        },
      }).then((res) => {
        // console.log(res.data);
        this.article_list = res.data.data;
        this.total = res.data.total;
      });
    },
    currentChange(val) {
      // console.log("第" + val + "页");
      this.currentPage = val;
      this.getListData(val);
    },
    remove(_, data) {
      console.log(data.id);
      axios({
        url: "http://127.0.0.1:9000/api/dweb-lanmu/",
        method: "delete",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: Qs.stringify({
          token: this.$store.getters.isnotUserlogin,
          id: data.id,
        }),
      }).then((res) => {
        console.log(res.data);
        if (res.data == "nologin") {
          alert("尚未登录");
          return;
        }
        if (res.data == "noperm") {
          alert("权限不足");
          return;
        }
        if (res.data == "ok") {
          this.getLanmuTree();
        }
      });
    },
    renderContent(h, { node, data }) {
      return (
        <span class="custom-tree-node">
          
          <span>{node.label}</span>
          <span> ({node.data.article_num})</span>
          <span>
            <el-button
              size="mini"
              type="text"
              style="margin-left:20px"
              on-click={() => this.remove(node, data)}
            >
              删除
            </el-button>
          </span>
        </span>
      );
    },
  },
};
</script>

<style scoped>
.dweb {
  padding: 10px 10px;
}
.card.dweb .text-item {
  color: #fff;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.text-item span {
  height: 40px;
  line-height: 20px;
  text-overflow: ellipsis;
  overflow: hidden;
}
.save-tree button {
  margin: 5px 5px;
}
</style>

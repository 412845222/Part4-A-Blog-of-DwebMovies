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
        <h5>新建用户组</h5>
        <el-divider></el-divider>
      </div>

      <el-row :gutter="10">
        <el-col :xs="24" :lg="12">
          <div class="new-group dweb">
            <el-form :inline="true" :model="new_group" class="demo-form-inline">
              <el-form-item>
                <el-input
                  v-model="new_group.name"
                  placeholder="新用户组名称"
                ></el-input>
              </el-form-item>
              <el-form-item>
                <el-button @click="saveNewGroup()" type="primary"
                  >保存</el-button
                >
              </el-form-item>
            </el-form>
          </div>
        </el-col>
        <el-col :xs="24" :lg="12">
          <div class="perm-list dweb">
            <el-row>
              <el-col
                v-for="(item, index) in new_group.checkList"
                :key="index"
                :span="24"
                style="border-bottom:1px solid #fff;padding:5px 0;"
              >
                <el-button
                  @click="chooseAllmethod(index)"
                  type="primary"
                  plain
                  style="float:left;margin-right:10px"
                  >{{ item.name }}</el-button
                >
                <el-checkbox-group v-model="item.checkList" style="float:left">
                  <el-checkbox
                    v-for="method in item.perm_methods"
                    :key="method.codename"
                    :label="method.codename"
                  >
                    {{ method.name }}
                  </el-checkbox>
                </el-checkbox-group>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>

      <div class="body dweb">
        <h5>所有用户组</h5>
        <el-divider></el-divider>
      </div>

      <div class="body dweb">
        <el-row>
          <el-col
            v-for="(item, index) in all_groups"
            :key="index"
            :xs="12"
            :lg="4"
          >
            <el-button-group>
              <el-button
                v-if="index == choosed_group"
               @click="chooseGroup(index)" type="warning">{{ item.name }}</el-button>
               <el-button
                v-else
               @click="chooseGroup(index)" type="primary">{{ item.name }}</el-button>
              <el-button
                @click="deleteGroup(item.name)"
                type="danger"
                icon="el-icon-delete"
              ></el-button>
            </el-button-group>
          </el-col>
        </el-row>
      </div>

      <div class="body dweb">
        <h5>用户列表</h5>
        <el-divider></el-divider>
      </div>

      <el-row :gutter="10">
        <el-col :span="16">
          <div class="body dweb">
            <el-transfer
              filterable
              :filter-method="filterMethod"
              filter-placeholder="请输入用户名"
              v-model="choosed_user"
              :data="userlist"
            >
            </el-transfer>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="body dweb">
            <el-button @click="setUserToGroup()" type="success" round>保存分配</el-button>
          </div>
          
        </el-col>
      </el-row>

      <div class="body dweb">
        <h5>当前用户分配</h5>
        <el-divider></el-divider>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Qs from "qs";
export default {
  data() {
    return {
      new_group: {
        name: "",
        checkList: [
          {
            name: "文章管理",
            content_type: "blog_article",
            perm_methods: [
              {
                name: "增",
                codename: "add",
              },
              {
                name: "删",
                codename: "delete",
              },
              {
                name: "改",
                codename: "change",
              },
              {
                name: "查",
                codename: "view",
              },
            ],
            checkList: [],
          },
          {
            name: "用户管理",
            content_type: "auth_user",
            perm_methods: [
              {
                name: "增",
                codename: "add",
              },
              {
                name: "删",
                codename: "delete",
              },
              {
                name: "改",
                codename: "change",
              },
              {
                name: "查",
                codename: "view",
              },
            ],
            checkList: [],
          },
          {
            name: "栏目管理",
            content_type: "blog_lanmu",
            perm_methods: [
              {
                name: "增",
                codename: "add",
              },
              {
                name: "删",
                codename: "delete",
              },
              {
                name: "改",
                codename: "change",
              },
              {
                name: "查",
                codename: "view",
              },
            ],
            checkList: [],
          },
        ],
      },
      all_groups: [],

      //用户列表 分配
      userlist: [],
      choosed_user: [],
      choosed_group:0,
      filterMethod(query, item) {
        return item.name.indexOf(query) > -1;
      },
    };
  },
  mounted() {
    this.getAllUserGroup();
    this.getUserList();
  },
  methods: {
    //保存分配用户 用户组
    setUserToGroup(){
      
      let group = this.all_groups[this.choosed_group]
      let userlist = this.choosed_user

      if (userlist.length==0) {
        alert("没有选择用户")
        return
      }

      //提交用户组分配
      axios({
        url:"https://api.study.dweb.club/api/dweb-group/",
        method:"post",
        data:Qs.stringify({
          token:this.$store.getters.isnotUserlogin,
          group:group.name,
          userlist:JSON.stringify(userlist)
        })
      }).then((res)=>{
        console.log(res.data)
        if (res.data == "nologin") {
          alert("尚未登录");
          return;
        }
        if (res.data == "noperm") {
          alert("权限不足");
          return;
        }
        if (res.data=="ok") {
          alert("用户权限分配成功")
          return
        }
      })
      

    },
    //选择用户组
    chooseGroup(index){
      this.choosed_group = index
    },
    //用户列表
    getUserList() {
      axios({
        url: "https://api.study.dweb.club/api/dweb-userlist/",
        method: "get",
      }).then((res) => {
        console.log(res.data);
        let userlist = res.data;
        userlist.forEach((user) => {
          this.userlist.push({
            label: user.name,
            key: user.name,
            name: user.name,
          });
        });
      });
    },
    //获取所有用户组
    getAllUserGroup() {
      axios({
        url: "https://api.study.dweb.club/api/dweb-group/",
        method: "get",
      }).then((res) => {
        console.log(res.data);
        this.all_groups = res.data;
      });
    },
    //删除用户组
    deleteGroup(name) {
      axios({
        url: "https://api.study.dweb.club/api/dweb-group/",
        method: "delete",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: Qs.stringify({
          name: name,
          token: this.$store.getters.isnotUserlogin,
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
          this.getAllUserGroup();
        }
      });
    },
    saveNewGroup() {
      //判断名称输入
      if (this.new_group.name.length == 0) {
        alert("输入新用户名称");
        return;
      }
      //判断权限的选择
      let checkType = false;
      let perm_list = [];
      this.new_group.checkList.forEach((obj) => {
        if (obj.checkList.length > 0) {
          checkType = true;
          let perm_item = {
            content_type: obj.content_type,
            perm_methods: obj.checkList,
          };
          perm_list.push(perm_item);
        }
      });
      if (checkType) {
        //执行提交
        let checkInfo = {
          contentType: "auth_user",
          permissions: ["add", "change", "delete", "view"],
        };
        this.$store.dispatch("checkUserPerm", checkInfo).then((res) => {
          if (res) {
            axios({
              url: "https://api.study.dweb.club/api/dweb-group/",
              method: "put",
              data: Qs.stringify({
                token: this.$store.getters.isnotUserlogin,
                new_group: this.new_group.name,
                perm_list: JSON.stringify(perm_list),
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
              if (res.data == "same name") {
                alert("重复命名");
                return;
              }
              if (res.data == "ok") {
                this.getAllUserGroup();
              }
            });
          }
        });
      } else {
        alert("新用户组 权限未选择");
        return;
      }
    },
    //全选 权限多选框
    chooseAllmethod(index) {
      if (this.new_group.checkList[index].checkList.length == 0) {
        this.new_group.checkList[index].checkList = [
          "add",
          "delete",
          "change",
          "view",
        ];
      } else {
        this.new_group.checkList[index].checkList = [];
      }
    },
  },
};
</script>

<style scoped>
.dweb {
  padding: 10px 10px;
}
.new-group {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.perm-list {
  height: 200px;
  overflow-y: scroll;
}
</style>

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
        <el-col :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span
                  >【CSS3】听说你们喜欢这种？ 一个炫彩渐变样式的搬砖与应用</span
                >
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>
                  发布者：admin
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span
                  >【CSS3】听说你们喜欢这种？ 一个炫彩渐变样式的搬砖与应用</span
                >
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>
                  发布者：admin
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span
                  >【CSS3】听说你们喜欢这种？ 一个炫彩渐变样式的搬砖与应用</span
                >
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>
                  发布者：admin
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span
                  >【CSS3】听说你们喜欢这种？ 一个炫彩渐变样式的搬砖与应用</span
                >
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>
                  发布者：admin
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
        <el-col :span="24">
          <div class="card dweb">
            <el-row>
              <el-col :xs="24" :lg="6">
                <el-image
                  v-if="screenWidth > 500"
                  style="height:100px"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
                <el-image
                  v-else
                  style="width:100%"
                  :src="
                    'https://api.dweb.club/upload/saved/926609164_cover.jpg'
                  "
                  :fit="'cover'"
                ></el-image>
              </el-col>
              <el-col class="text-item" :xs="24" :lg="4">
                <span
                  >【CSS3】听说你们喜欢这种？ 一个炫彩渐变样式的搬砖与应用</span
                >
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <span>
                  发布者：admin
                </span>
              </el-col>
              <el-col class="text-item" :xs="12" :lg="7">
                <el-button
                  type="success"
                  icon="el-icon-search"
                  circle
                ></el-button>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 分页器 -->
    <div class="dweb" style="margin-top:10px">
      <el-pagination background layout="prev, pager, next" 
        :total="total"
        :page-size="pageSize"
        @current-change="currentChange"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  props: ["screenWidth"],
  data() {
    return {
      currentPage:1,
      pageSize:20,
      total: 100,
    };
  },
  methods: {
    currentChange(val){
      console.log('第'+val+'页')
    }
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

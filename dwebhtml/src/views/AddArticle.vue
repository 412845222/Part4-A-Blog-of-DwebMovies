<template>
  <div id="add-article">
    <el-row :gutter="10">
      <el-col :xs="24" :lg="8">
        <div class="dweb">
          <el-form
            :label-position="'left'"
            label-width="80px"
            :model="article_info"
          >
            <el-form-item label="文章标题">
              <el-input v-model="article_info.title"></el-input>
            </el-form-item>
            <el-form-item label="描述">
              <el-input
                type="textarea"
                :rows="4"
                v-model="article_info.describe"
              ></el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :xs="24" :lg="16">
        <div class="dweb">
          <div v-for="(img, index) in cover_list" :key="index">
            <el-image
              style="width: 100px; height: 100px"
              :src="img"
              :fit="'cover'"
            ></el-image>
          </div>
          <el-button type="success" round>保存文章</el-button>
        </div>
      </el-col>
      <el-col :xs="24" :lg="24">
        <div class="dweb">
          <div id="summernote"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  data() {
    return {
      article_info: {
        title: "",
        describe: "",
      },
      cover_list: [],
    };
  },
  mounted() {
    this.summernote();
  },
  methods: {
    summernote() {
      let self = this;
      $("#summernote").summernote({
        width: "100%",
        height: 500,
        lang: "zh-CN",
        callbacks: {
          //当输入
          onChange(contents) {
            console.log(contents);
          },
          //本地图片上传
          onImageUpload(files) {
            //  console.log(files)
            let img = files[0];
            let imgData = new FileReader();
            imgData.readAsDataURL(img);
            console.log(imgData);
            imgData.onload = function() {
              console.log(imgData.result);
              //插入图片本身
              let imgnode = document.createElement('img')
              imgnode.src = imgData.result
              $("#summernote").summernote('insertNode',imgnode)
              //推入封面待选择
              self.cover_list.push(imgData.result);
            };
          },
          //远程图片添加
          onImageLinkInsert(url){
            console.log(url)
            let imgnode = document.createElement('img')
            imgnode.src = url
            console.log(imgnode)
          }
          
        },
      });
    },
  },
};
</script>

<style scoped>
.dweb {
  min-height: 200px;
  padding: 20px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-form-item {
  margin-top: 22px;
}
.dweb .el-button {
  position: fixed;
  right: 20px;
  z-index: 1001;
  margin-top: 280px;
}
</style>

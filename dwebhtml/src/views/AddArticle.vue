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
              <el-input type="textarea" v-model="article_info.describe"></el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
      <el-col :xs="24" :lg="16">
        <div class="dweb"></div>
      </el-col>
      <el-col :xs="24" :lg="24">
        <div class="dweb">
          <div id="summernote">Hello Summernote</div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  data() {
    return {
      article_info:{
        title:'',
        describe:''
      }
    }
  },
  mounted() {
    this.summernote()
  },
  methods: {
    summernote(){
       $('#summernote').summernote({
         height: 500,
         lang: 'zh-CN'
       });
    }
  },
};
</script>

<style scoped>
.dweb {
  /* height: 200px; */
  padding: 20px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.el-form-item {
  margin-top: 22px;
}


</style>

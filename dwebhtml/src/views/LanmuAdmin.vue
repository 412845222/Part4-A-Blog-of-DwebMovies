<template>
  <div>
    <!-- 面包屑导航 -->
    <BreadMenu :page_name="'栏目管理'"></BreadMenu>
  </div>
</template>

<script>
import BreadMenu from "../components/BreadMenu"
export default {
  data() {
    return {
      
    }
  },
  components:{
    BreadMenu
  }
}
</script>

<style scoped>

</style>
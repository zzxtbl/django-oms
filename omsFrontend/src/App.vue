<template>
	<div id="app">
		<router-view></router-view>
    <el-tooltip placement="top" content="一路向西">
      <back-to-top transitionName="fade" :customStyle="BackToTopStyle" :visibilityHeight="300" :backPosition="50"></back-to-top>
    </el-tooltip>
	</div>
</template>

<script>
import BackToTop from '@/components/BackToTop'

export default{
  name: 'APP',
  components: { BackToTop },
  data() {
    return {
      BackToTopStyle: {
        right: '50px',
        bottom: '50px',
        width: '40px',
        height: '40px',
        'border-radius': '50px',
        'line-height': '45px', // 请保持与高度一致以垂直居中
        'z-index': 1024
      }
    }
  }
}
</script>

<style lang="scss">
@import '~normalize.css/normalize.css'; // normalize.css 样式格式化
@import './styles/index.scss'; // 全局自定义样式
</style>

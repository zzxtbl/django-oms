<template>
  <div class="components-container" style='height:100vh'>
    <el-tabs type="border-card">
      <el-tab-pane v-for="item in tableData" :key="item.id" :label="item.name">
        <div class="category">
          <p><i class="el-icon-location"></i>{{item.name}}</p>
          <ul>
            <li class="new-task-item clearfix" v-for="t in item.process" :key="t.pk">
              <a href="/" target="_blank">{{t.fields.name}}</a>
            </li>
          </ul>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getWfcategory } from 'api/workflow'

export default {
  components: {},
  data() {
    return {
      tableData: []
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getWfcategory().then(response => {
        this.tableData = response.data
      })
    }
  }
}
</script>

<style lang='scss'>
  .category {
    p {
      font-size: 20px;
      font-weight: 700;
    }
    .new-task-item {
      color: #8E8E8E;
      line-height: 27px;
      height: 52px;
      border: 1px solid #DDD;
      margin: 5px 5px 5px -30px;
      padding: 10px;
      border-left: 5px solid #609ACA;
      background: #FFF;
      border-radius: 5px;
      list-style: none;
      &:hover {
        background-color: #fafafa;
      }
    }
  }
</style>

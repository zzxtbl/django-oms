<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
        </div>
        <div class="table-search">
          <el-input
            placeholder="搜索 ..."
            v-model="listQuery.search"
            @keyup.enter.native="searchClick">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table v-loading="dataloading"
                  element-loading-text="让子弹飞一会儿"
                  element-loading-background="rgba(0, 0, 0, 0.8)"
                  :data='tableData' border style="width: 100%">
          <el-table-column prop='groupid' label='id'></el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='hosts' label='包含主机'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag v-for="item in scope.row.hosts" :key="item.hostid" size="mini" style="margin-right: 3px">
                  <a v-if="item.status==1" style="color: red">{{item.host}}</a>
                  <a v-else>{{item.host}}</a>
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <!--<el-table-column label="操作">-->
          <!--<template slot-scope="scope">-->
          <!--<el-button @click="deleteGroup(scope.row.id)" type="danger" size="small">删除</el-button>-->
          <!--</template>-->
          <!--</el-table-column>-->
        </el-table>
      </div>
      <div class="table-pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="pagesize"
          :page-size="listQuery.limit"
          :layout="pageformat"
          :total="tabletotal">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getzkHostGroup } from 'api/zabbix'
import { LIMIT, pagesize, pageformat } from '@/config'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      listQuery: {
        limit: LIMIT,
        offset: 0,
        search: ''
      },
      dataloading: true
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getzkHostGroup(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        this.dataloading = false
      })
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = val - 1
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>

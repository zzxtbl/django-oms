<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-button type="primary" icon="el-icon-plus" @click="addForm=true">新建</el-button>
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
          <el-table-column prop='hostid' label='id'></el-table-column>
          <el-table-column prop='host' label='主机名'></el-table-column>
          <el-table-column prop='status' label='状态'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='groups' label='所在组'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag v-for="item in scope.row.groups" :key="item.groupid" size="mini" style="margin-right: 3px">
                  {{item.name}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='interfaces' label='监听地址'>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper" style="text-align: center">
                <el-tag size="mini" style="margin-right: 3px">
                  {{scope.row.interfaces[0].ip}}:{{scope.row.interfaces[0].port}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button-group>
                <el-button type="success" size="small">修改</el-button>
                <el-button type="danger" size="small">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
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

    <el-dialog :visible.sync="addForm">
      <el-form :model="ruleForm" ref="ruleForm" label-width="100px">
        <el-form-item label="主机名ip" prop="hostnames">
          <el-input v-model="hostnames" type="textarea" placeholder="sh-aa-01|sh-bb-02"
                    :autosize="{ minRows: 3, maxRows: 5}"></el-input>
        </el-form-item>
        <el-form-item label="主机组" prop="hostgroups">
          <sesect-groups :selectdata="ruleForm.hostgroups" @getDatas="getGroups"></sesect-groups>
        </el-form-item>
        <el-form-item label="模板" prop="templates">
          <sesect-temps :selectdata="ruleForm.templates" @getDatas="getTemps"></sesect-temps>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="CreateGroup('ruleForm')">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getzkHost, postzkHost } from 'api/zabbix'
import { LIMIT, pagesize, pageformat } from '@/config'
import sesectGroups from './components/grouptransfer.vue'
import sesectTemps from './components/temptransfer.vue'

export default {
  components: {
    sesectGroups, sesectTemps
  },
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
      STATUS_COLOR: { 0: 'success', 1: 'danger' },
      STATUS_TEXT: { 0: 'enabled', 1: 'disabled' },
      dataloading: true,
      addForm: false,
      ruleForm: {
        hostnames: [],
        hostgroups: [],
        templates: []
      },
      hostnames: '',
      groupdatas: [],
      tempdatas: []
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getzkHost(this.listQuery).then(response => {
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
    },
    getGroups(data) {
      this.ruleForm.hostgroups = data
    },
    getTemps(data) {
      this.ruleForm.templates = data
    },
    CreateGroup() {
      this.ruleForm.action = 'create'
      this.ruleForm.hostnames = this.hostnames.split('|')
      postzkHost(this.ruleForm).then(response => {
        let offset = 12
        for (const item of response.data) {
          offset *= 3
          this.$notify({
            title: item.title,
            message: item.message,
            type: item.type,
            offset: offset
          })
        }
        this.fetchData()
        this.addForm = false
      }).catch(error => {
        const errordata = JSON.stringify(error.response.data)
        this.$message.error(errordata)
      })
    }
  }
}
</script>

<style lang='scss'>

</style>

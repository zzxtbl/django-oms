<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <router-link :to="'addopsdemand'">
            <el-button type="primary" icon="el-icon-plus">新建</el-button>
          </router-link>
          <el-button type="danger" size="small" @click="showAll">全部</el-button>
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-input style="width: 180px;" placeholder="编号、标题、内容"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 100%" @sort-change="handleSortChange">
          <el-table-column prop='pid' label='编号'>
            <template slot-scope="scope">
              <div slot="reference">
                <router-link :to="'viewopsdemand/' + scope.row.id">
                  <a style="color: #257cff">{{scope.row.pid}}</a>
                </router-link>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='name' label='名称'></el-table-column>
          <el-table-column prop='start_time' label='开始日期' sortable="custom">
            <template slot-scope="scope">
              <a v-if="scope.row.is_ci">持续项目</a>
              <a v-else>{{scope.row.start_time}}</a>
            </template>
          </el-table-column>
          <el-table-column prop='end_time' label='结束日期'>
            <template slot-scope="scope">
              <a v-if="scope.row.is_ci">持续项目</a>
              <a v-else>{{scope.row.end_time}}</a>
            </template>
          </el-table-column>
          <el-table-column prop='status' label='状态' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <el-tag size="mini" :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
                <el-tooltip class="item" effect="dark" content="更改状态" placement="top">
                  <el-button v-if="scope.row.status!=1 & !scope.row.is_ci" type="text" icon="el-icon-edit"
                             class="modifychange"
                             @click="updateDemand(scope.row.id)"></el-button>
                </el-tooltip>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='task_complete' label='项目进度' sortable="custom">
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                <a v-if="scope.row.is_ci">持续项目</a>
                <a v-else>{{scope.row.task_complete}}%</a>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template slot-scope="scope">
              <el-button-group v-if="scope.row.status==0">
                <router-link :to="'/opstasks/editopsdemand/' + scope.row.id">
                  <el-button type="success" size="mini">修改</el-button>
                </router-link>
                <!--<el-button type="primary" size="mini" @click="addProject(scope.row)">增加任务</el-button>-->
                <el-button type="danger" size="mini" @click="deleteDemand(scope.row.id)">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-footer">
        <div class="table-button">
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
      </div>
    </el-card>

    <el-dialog :visible.sync="demandstatusForm">
      <el-form label-width="90px">
        <el-form-item label="更改状态" prop="status">
          <el-radio-group v-model="updateform.status">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changeDemandStatus">确 定</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDemandManager,
  deleteDemandManager,
  patchDemandManager,
  getProject
} from '@/api/optask'
import { LIMIT, pagesize, pageformat } from '@/config'
import addProject from './components/addproject.vue'
import VueMarkdown from 'vue-markdown' // 前端解析markdown
import { getUser } from 'api/user'

export default {
  components: { VueMarkdown, addProject },
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      STATUS_TEXT: { 0: '进行中', 1: '已完成', 2: '搁置' },
      STATUS_COLOR: { 0: 'primary', 1: 'success', 2: 'warning' },
      listQuery: {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '0',
        create_user__username: '',
        search: '',
        ordering: ''
      },
      demandstatusForm: false,
      updateform: {
        id: '',
        status: '1'
      },
      users: []
    }
  },
  created() {
    this.fetchData()
    this.getUsers()
  },

  methods: {
    fetchData() {
      getDemandManager(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        this.tableData.map(function(item) {
          const parmas = {
            demand__id: item.id
          }
          getProject(parmas).then(res => {
            item.projectData = res.data
            item.task_complete = 0
            for (const pp of res.data) {
              item.task_complete += pp.task_complete
            }
            item.task_complete = Math.round(item.task_complete / res.data.length)
            let data
            if (item.task_complete) {
              data = {
                task_complete: item.task_complete
              }
            } else {
              data = {
                task_complete: 0
              }
            }
            patchDemandManager(item.id, data)
          })
        })
      })
    },
    showAll() {
      this.listQuery = {
        limit: LIMIT,
        offset: '',
        pid: '',
        status: '',
        create_user__username: '',
        search: '',
        ordering: ''
      }
      this.fetchData()
    },
    searchClick() {
      this.fetchData()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    changeStatus() {
      this.fetchData()
    },
    handleSortChange(val) {
      if (val.order === 'ascending') {
        this.listQuery.ordering = val.prop
      } else if (val.order === 'descending') {
        this.listQuery.ordering = '-' + val.prop
      } else {
        this.listQuery.ordering = ''
      }
      this.fetchData()
    },
    deleteDemand(id) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteDemandManager(id).then(response => {
          this.$message({
            message: '恭喜你，删除成功',
            type: 'success'
          })
          this.fetchData()
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    updateDemand(id) {
      this.demandstatusForm = true
      this.updateform.id = id
    },
    changeDemandStatus() {
      patchDemandManager(this.updateform.id, this.updateform).then(() => {
        this.demandstatusForm = false
        this.fetchData()
      })
    },
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    }
  }
}
</script>

<style lang='scss'>
  .modifychange {
    margin: 5px;
  }
</style>

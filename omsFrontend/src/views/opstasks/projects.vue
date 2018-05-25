<template>
  <div class="components-container" style='height:100vh'>
    <el-card>
      <div class="head-lavel">
        <div class="table-button">
          <el-radio-group v-model="listQuery.status" @change="changeStatus" style="margin-left: 20px">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </div>
        <div class="table-search">
          <el-date-picker
            v-model="selectcreatedate"
            type="daterange"
            range-separator="至"
            start-placeholder="创建日期"
            end-placeholder="结束日期"
            @change="selectCreatedate"
            :picker-options="pickerOptions">
          </el-date-picker>
          <el-date-picker
            v-model="selectupdatedate"
            type="daterange"
            range-separator="至"
            start-placeholder="修改日期"
            end-placeholder="结束日期"
            @change="selectUpdatedate"
            :picker-options="pickerOptions">
          </el-date-picker>
          <el-input style="width: 200px;" placeholder="编号、标题、内容"
                    @keyup.enter.native="searchClick"
                    v-model="listQuery.search">
            <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
          </el-input>
        </div>
      </div>
      <div>
        <el-table :data='tableData' border style="width: 100%">
          <el-table-column prop="pid" label="编号" width="153"></el-table-column>
          <el-table-column prop="demand" label="关联项目" width="153"></el-table-column>
          <el-table-column prop="name" label="任务概要"></el-table-column>
          <el-table-column prop="action_user" label="负责人"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template slot-scope="scope">
              <div slot="reference">
                <el-tag size="mini" :type="STATUS_COLOR[scope.row.status]">
                  {{STATUS_TEXT[scope.row.status]}}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="task_complete" label="进度" sortable>
            <template slot-scope="scope">
              <div slot="reference" class="name-wrapper">
                {{scope.row.task_complete}}%
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='create_time' label='创建时间' sortable="custom" width="152">
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.create_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop='update_time' label='修改时间' sortable="custom" width="152">
            <template slot-scope="scope">
              <div slot="reference" style="text-align: center; color: rgb(0,0,0)">
                <span>{{scope.row.update_time | parseDate}}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button-group>
                <el-button type="success" plain size="mini" @click=editComplete(scope.row)>进度</el-button>
                <el-button @click="deleteGroup(scope.row.id)" type="danger" size="mini">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="table-pagination">
        <el-pagination
          small
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

    <el-dialog title="任务进度" :visible.sync="editForm">
      <el-form label-width="90px">
        <el-form-item label="完成百分比">
          <el-slider
            style="margin-right: 50px"
            v-model="completeform.task_complete"
            :step="10">
          </el-slider>
          <a>{{completeform.task_complete}}%</a>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="completeform.status">
            <el-radio v-for="item in Object.keys(STATUS_TEXT)" :key="item" :label="item">{{STATUS_TEXT[item]}}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="进度详情">
          <el-input v-model="commentform.content" type="textarea" :rows="2" placeholder="请输入进度详情"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="addComment" type="success" size="mini">添加</el-button>
          <el-button @click="updateComplete" type="primary" size="mini">确定</el-button>
        </el-form-item>
      </el-form>
      <template>
        <light-timeline :items='commentData'></light-timeline>
      </template>
    </el-dialog>

    <el-dialog title="任务进度" :visible.sync="onlyView">
      <el-progress v-if="completeform.task_complete==100" :text-inside="true" :stroke-width="18" :percentage="100"
                   status="success"></el-progress>
      <light-timeline :items='commentData'></light-timeline>
    </el-dialog>

  </div>
</template>

<script>
import { getProject, deleteProject, patchProject, postProjectComment, getProjectComment } from 'api/optask'
import { LIMIT, pagesize, pageformat } from '@/config'
import formatDate from '@/utils/dateformat'

export default {
  components: {},
  data() {
    return {
      tableData: [],
      tabletotal: 0,
      searchdata: '',
      currentPage: 1,
      pagesize: pagesize,
      pageformat: pageformat,
      listQuery: {
        limit: LIMIT,
        offset: '',
        status: '',
        search: ''
      },
      STATUS_TEXT: { 0: '进行中', 1: '已完成', 2: '搁置' },
      STATUS_COLOR: { 0: 'primary', 1: 'success', 2: 'warning' },
      editForm: false,
      completeform: {
        id: '',
        status: '',
        task_complete: ''
      },
      commentform: {
        project: '',
        content: '',
        create_user: localStorage.getItem('username')
      },
      commentData: [],
      selectcreatedate: '',
      selectupdatedate: '',
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      },
      onlyView: false
    }
  },

  created() {
    this.fetchData()
  },

  methods: {
    fetchData() {
      getProject(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
      })
    },
    fetchCommentData(pid) {
      const data = {
        project__id: pid
      }
      getProjectComment(data).then(response => {
        this.commentData = response.data
        this.commentData.map(function(item) {
          const c_time = item.create_time
          const date = c_time.slice(0, 10)
          const time = c_time.slice(11, 19)
          item.tag = date + ' ' + time
        })
      })
    },
    deleteGroup(id) {
      this.$confirm('你确定要删除这个, 是否继续?', '美丽的妲己提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteProject(id).then(response => {
          this.$message({
            message: '恭喜你，删除成功',
            type: 'success'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    editComplete(row) {
      if (row.task_complete === 100) {
        this.onlyView = true
      } else {
        this.editForm = true
      }
      this.completeform.id = this.commentform.project = row.id
      this.completeform.task_complete = row.task_complete
      this.completeform.status = row.status.toString()
      this.fetchCommentData(this.completeform.id)
    },
    addComment() {
      postProjectComment(this.commentform).then(() => {
        this.fetchCommentData(this.completeform.id)
      })
    },
    updateComplete() {
      if (this.completeform.status !== '2') {
        if (this.completeform.task_complete === 100) {
          this.completeform.status = 1
        } else {
          this.completeform.status = 0
        }
      }
      patchProject(this.completeform.id, this.completeform).then(response => {
        this.fetchData()
        this.editForm = false
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
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchData()
    },
    changeStatus() {
      this.fetchData()
    },
    selectCreatedate(val) {
      if (val) {
        this.listQuery.create_date_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.create_date_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.create_date_0 = ''
        this.listQuery.create_date_1 = ''
      }
      this.fetchData()
    },
    selectUpdatedate(val) {
      if (val) {
        this.listQuery.update_date_0 = formatDate(val[0], 'YYYY-MM-DD')
        this.listQuery.update_date_1 = formatDate(val[1], 'YYYY-MM-DD')
      } else {
        this.listQuery.update_date_0 = ''
        this.listQuery.update_date_1 = ''
      }
      this.fetchData()
    }
  }
}
</script>

<style lang='scss'>

</style>

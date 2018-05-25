<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="title">{{ticketData.name}}</a>
            <hr class="heng"/>

            <div class="appendInfo">
              <a class="ticketinfo create_user"><span class="han">
                                创建时间：</span>{{ticketData.create_time | parseDate}}</a>
              <a class="ticketinfo create_user"><span class="han">
                              <a class="shu"></a>
                                创建人：</span>{{ticketData.create_user}}</a>
              <!--<a class="ticketinfo create_user"><span class="han">-->
              <!--<a class="shu"></a>-->
              <!--参与者：</span>-->
              <!--<el-tag style="margin-right: 2px" size="mini" v-for="item in ticketData.action_user" :key="item">{{item}}-->
              <!--</el-tag>-->
              <!--</a>-->
              <a class="shu"></a>
              <span class="han">计划开始日期：</span>
              <a class="ticketinfo">{{ticketData.start_time}}</a>
              <a class="shu"></a>
              <span class="han">计划完成日期：</span>
              <a class="ticketinfo">{{ticketData.end_time}}</a>
            </div>
          </div>
          <el-card>
            <div slot="header" class="clearfix">
              项目目标
            </div>
            <vue-markdown :source="ticketData.content1"></vue-markdown>
          </el-card>
          <el-card>
            <div slot="header" class="clearfix">
              项目范围
            </div>
            <a>{{ticketData.content2}}</a>
          </el-card>
          <el-card>
            <div slot="header" class="clearfix">
              项目预算
            </div>
            <a>{{ticketData.content3}}</a>
          </el-card>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header" class="clearfix">
            <a class="right-title">任务列表</a>
            <el-button class="card-head-btn" type="text" icon="el-icon-plus" @click="addForm=true"></el-button>
          </div>
          <el-table :data="projectData" stripe style="width: 100%">
            <el-table-column type="index" width="50"></el-table-column>
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="status" label="状态" width="70">
              <template slot-scope="scope">
                <div slot="reference">
                  <el-tag size="mini" :type="STATUS_COLOR[scope.row.status]">{{STATUS_TEXT[scope.row.status]}}</el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="complete" label="操作" width="150">
              <template slot-scope="scope">
                <el-button-group>
                  <el-button type="success" plain size="mini" @click=editComplete(scope.row)>进度</el-button>
                  <el-button @click="deleteGroup(scope.row.id)" type="danger" size="mini">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog :visible.sync="addForm">
      <add-project :demand="ticketData" @DialogStatus="getDialogStatus"></add-project>
    </el-dialog>

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
import {
  getDemandManager,
  getProject,
  patchProject,
  postProjectComment,
  deleteProject,
  getProjectComment
} from '@/api/optask'
import { apiUrl } from '@/config'
import addProject from './addproject.vue'
import VueMarkdown from 'vue-markdown'

export default {
  components: {
    addProject, VueMarkdown
  },

  data() {
    return {
      pid: this.$route.params.id,
      ticketData: {},
      STATUS_TEXT: { 0: '进行中', 1: '已完成', 2: '搁置' },
      STATUS_COLOR: { 0: 'primary', 1: 'success', 2: 'warning' },
      apiurl: apiUrl,
      projectData: [],
      addForm: false,
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
      onlyView: false
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      const query = null
      getDemandManager(query, this.pid).then(response => {
        this.ticketData = response.data
        this.fetchProjectData()
      })
    },
    fetchProjectData() {
      const data = {
        demand__id: this.pid
      }
      getProject(data).then(response => {
        this.projectData = response.data
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
    getDialogStatus(data) {
      this.addForm = data
      this.editForm = data
      this.fetchData()
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
    }
  }
}
</script>

<style lang='scss'>
  .editticket {
    margin: 50px;
    width: 80%;
  }

  .title {
    font-size: 28px;
    font-weight: 700;
    padding-left: 10px;
  }

  .right-title {
    font-size: 20px;
    font-weight: 600;
    padding-left: 10px;
  }

  .card-head-btn {
    float: right;
    padding: 3px 0;
  }

  .appendInfo {
    padding: 5px;
    margin: 5px;
  }

  .action {
    margin: 5px;
  }

  .han {
    margin-left: 5px;
  }
</style>

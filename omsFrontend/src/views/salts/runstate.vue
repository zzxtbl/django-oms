<template>
  <div class="components-container" style='height:100vh'>
    <el-row :gutter="20">
      <el-col :span="10">
        <el-card>
          <div slot="header">
            <span>执行state</span>
          </div>
          <el-form :model="ruleForm" ref="ruleForm" label-width="70px">
            <el-form-item label="选择主机" prop="hosts">
              <sesect-hosts :selecthost="ruleForm.hosts" @gethosts="getHosts"></sesect-hosts>
            </el-form-item>
            <hr class="heng"/>
            <el-form-item v-for="item in stategroups" :key="item.id" :label="item.name">
              <el-button v-for="cmd in item.cmds" :key="cmd.id" size="mini" @click="ruleForm.selectcmd=cmd.cmd">
                {{cmd.name}}
              </el-button>
            </el-form-item>
            <hr class="heng"/>
            <el-form-item>
              <el-button type="primary" @click="submitForm('ruleForm')">执行</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="14">
        <el-card>
          <div class="table-button">
            <a class="jobname">历史记录</a>
          </div>
          <div class="table-search">
            <el-input
              placeholder="search"
              v-model="listQuery.search"
              @keyup.enter.native="searchClick">
              <i class="el-icon-search el-input__icon" slot="suffix" @click="searchClick"></i>
            </el-input>
          </div>
          <div>
            <el-table :data='tableData' @selection-change="handleSelectionChange" style="width: 100%">
              <el-table-column type="selection" v-if="role==='super'"></el-table-column>
              <el-table-column prop='statejob' label='名称'></el-table-column>
              <el-table-column prop='status' label='状态' sortable>
                <template slot-scope="scope">
                  <div slot="reference">
                    <el-button plain size="mini" :type="DEPLOY_STATUS[scope.row.deploy_status].type"
                               :icon="DEPLOY_STATUS[scope.row.deploy_status].icon">
                      {{DEPLOY_STATUS[scope.row.deploy_status].text}}
                    </el-button>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop='action_user' label='发布人'></el-table-column>
              <el-table-column prop='create_time' label='发布时间' sortable>
                <template slot-scope="scope">
                  <div slot="reference">
                    {{scope.row.create_time | formatTime}}
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button @click="showJobResult(scope.row.result)" type="success" size="mini"
                             :disabled="!scope.row.result">结果
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div class="table-footer">

            <div class="table-button" v-if="role==='super'">
              <el-button type="danger" icon="delete" :disabled="butstatus" @click="deleteForm">删除记录</el-button>
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
      </el-col>
    </el-row>

    <el-dialog :visible.sync="showresult">
      <div>
        <div class="runlog" v-for="item in job_results" :key="item.id">
          <p class="host">{{ item.host }}</p>
          <pre>{{ item.data }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { deleteDeployJob, getUpdateJobsStatus } from '@/api/job'
import { getSaltStateGroup, getSaltState, getSaltStateJob } from 'api/salt'
import { mapGetters } from 'vuex'
import { LIMIT, pagesize, pageformat } from '@/config'
import sesectHosts from '../components/hosttransfer.vue'

export default {
  components: { sesectHosts },
  data() {
    return {
      selectcmd: '',
      route_path: this.$route.path.split('/'),
      job_id: this.$route.params.job_id,
      versionForm: {
        version: '',
        content: ''
      },
      ruleForm: {
        job: '',
        env: '',
        deploy_hosts: [],
        deploy_cmd: '',
        action_user: localStorage.getItem('username'),
        deploy_cmd_host: 'null'
      },
      steps: [],
      cur_env: {},
      cmds: [],
      jobs: {},
      sendnotice: false,
      hasversion: false,
      stepForm: {
        cur_step: 1,
        done: false
      },
      onlyread: false,
      checkAll: true,
      checkedcmds: [],
      currentPage: 1,
      listQuery: {
        limit: LIMIT,
        offset: '',
        search: ''
      },
      pagesize: pagesize,
      pageformat: pageformat,
      tableData: [],
      tabletotal: 0,
      DEPLOY_STATUS: {
        deploy: { text: '发布中', type: 'primary', icon: 'el-icon-loading' },
        success: { text: '发布成功', type: 'success', icon: 'el-icon-success' },
        failed: { text: '发布失败', type: 'danger', icon: 'el-icon-error' }
      },
      selectId: [],
      butstatus: true,
      showresult: false,
      job_results: [],
      check_job_status: '',
      deploy_cmds: [],
      stategroups: [],
      selecthosts: []
    }
  },
  computed: {
    ...mapGetters([
      'role'
    ])
  },
  created() {
    this.fetchGroupData()
    this.fetchJobData()
  },
  methods: {
    fetchGroupData() {
      getSaltStateGroup().then(response => {
        this.stategroups = response.data
        this.stategroups.map(function(data) {
          const parmas = {
            group__name: data.name
          }
          getSaltState(parmas).then(response => {
            data['cmds'] = response.data
          })
        })
      })
    },
    fetchJobData() {
      getSaltStateJob(this.listQuery).then(response => {
        this.tableData = response.data.results
        this.tabletotal = response.data.count
        const job_status = this.tableData.map(function(item) {
          return item.status
        })
        if (job_status.indexOf('deploy') > -1) {
          this.check_job_status = setInterval(() => {
            const pramas = {
              job__id: this.job_id
            }
            getUpdateJobsStatus(pramas).then(response => {
              if (response.data.count === 0) {
                clearInterval(this.check_job_status)
                this.jobs.done = true
                this.fetchDeployJobData()
              } else {
                console.log('check job_status 3/s')
              }
            })
          }, 3000)
        } else {
          console.log('setInterval_id:' + this.check_job_status)
          clearInterval(this.check_job_status)
        }
      })
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchDeployJobData()
    },
    handleCurrentChange(val) {
      this.listQuery.offset = (val - 1) * LIMIT
      this.fetchDeployJobData()
    },
    handleSelectionChange(val) {
      this.selectId = []
      for (var i = 0, len = val.length; i < len; i++) {
        this.selectId.push(val[i].id)
      }
      if (this.selectId.length > 0) {
        this.butstatus = false
      } else {
        this.butstatus = true
      }
    },
    deleteForm() {
      clearInterval(this.check_job_status)
      for (var i = 0, len = this.selectId.length; i < len; i++) {
        deleteDeployJob(this.selectId[i]).then(response => {
          delete this.selectId[i]
        })
      }
      setTimeout(this.fetchDeployJobData, 1000)
    },
    showJobResult(row) {
      this.showresult = true
      const data = (new Function('return ' + row))()
      const a = []
      Object.keys(data).map(function(k) {
        a.push({ 'host': k, 'data': data[k] })
      })
      this.job_results = a
    },
    searchClick() {
      this.fetchDeployJobData()
    },
    getHosts(data) {
      this.ruleForm.hosts = data
    }
  }
}
</script>

<style lang='scss'>
</style>

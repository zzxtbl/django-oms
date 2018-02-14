<template>
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="关联任务" prop="project">
      <el-select v-model="ruleForm.project" filterable placeholder="请选择关联任务">
        <el-option v-for="item in projects" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="关联test" prop="test">
      <el-select v-model="ruleForm.test" filterable placeholder="请选择关联test">
        <el-option v-for="item in tests" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="严重程度" prop="degree">
      <el-rate
        v-model="ruleForm.degree"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星星代表问题严重程度，星星越多，越严重</a>
    </el-form-item>
    <el-form-item label="优先级" prop="nice">
      <el-select v-model="ruleForm.nice" placeholder="请选择优先级">
        <el-option v-for="item in nices" :key="item.id" :label="item.label" :value="item.value"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试人员" prop="test_user">
      <el-select v-model="ruleForm.test_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="分配给" prop="action_user">
      <el-select v-model="ruleForm.action_user" filterable placeholder="请选择用户">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="测试时间" prop="test_time">
      <el-date-picker
        v-model="ruleForm.test_time"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="关闭时间" prop="end_time">
      <el-date-picker
        v-model="ruleForm.end_time"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期时间">
      </el-date-picker>
    </el-form-item>
    <el-form-item label="描述" prop="desc">
      <el-input v-model="ruleForm.desc" type="textarea" :autosize="{ minRows: 5, maxRows: 10}"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import { getUser } from 'api/user'
import { getProject, postBugManager, getTestManager } from '@/api/project'
export default {
  props: ['pname'],
  data() {
    return {
      ruleForm: {
        project: null,
        name: '',
        summary: '',
        degree: 2,
        nice: '',
        test_user: '',
        action_user: '',
        test_time: '',
        end_time: '',
        desc: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入一个正确的内容', trigger: 'blur' }
        ]
      },
      projects: [],
      nices: [
        { 'label': '低', value: '0' },
        { 'label': '中', value: '1' },
        { 'label': '高', value: '2' }
      ],
      users: [],
      tests: []
    }
  },
  created() {
    if (this.pname) {
      this.ruleForm.project = this.pname
    }
    this.getUsers()
    this.getProjects()
    this.getTest()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          postBugManager(this.ruleForm).then(response => {
            this.$message({
              message: '恭喜你，添加成功',
              type: 'success'
            })
            this.$emit('DialogStatus', false)
          }).catch(error => {
            this.$message.error('添加失败')
            console.log(error)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    getUsers() {
      const query = {
        groups__name: 'ITDept'
      }
      getUser(query).then(response => {
        this.users = response.data
      })
    },
    getProjects() {
      getProject().then(response => {
        this.projects = response.data
      })
    },
    getTest() {
      getTestManager().then(response => {
        this.tests = response.data
      })
    }
  }
}
</script>
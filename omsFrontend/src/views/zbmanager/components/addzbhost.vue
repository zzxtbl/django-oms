<template>
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
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
import sesectGroups from './grouptransfer.vue'
import sesectTemps from './temptransfer.vue'
import { postzkHost } from 'api/zabbix'

export default {
  components: { sesectGroups, sesectTemps },

  data() {
    return {
      ruleForm: {
        hostnames: [],
        hostgroups: [],
        templates: []
      },
      hostnames: ''
    }
  },
  created() {
  },
  methods: {
    submitForm(formName) {
      this.ruleForm.action = 'create'
      this.ruleForm.hostnames = this.hostnames.split('|')
      postzkHost(this.ruleForm).then(response => {
        let offset = 11
        for (const item of response.data) {
          offset *= 3
          this.$notify({
            title: item.title,
            message: item.message,
            type: item.type,
            offset: offset
          })
        }
        this.$emit('DialogStatus', false)
      }).catch(error => {
        const errordata = JSON.stringify(error.response.data)
        this.$message.error(errordata)
      })
    },
    getGroups(data) {
      this.ruleForm.hostgroups = data
    },
    getTemps(data) {
      this.ruleForm.templates = data
    }
  }
}
</script>

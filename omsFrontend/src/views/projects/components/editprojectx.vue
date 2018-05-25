<template>
  <el-form :model="rowdata" :rules="rules" ref="rowdata" label-width="100px">
    <el-form-item label="关联需求" prop="demand">
      <el-input v-model="rowdata.demand" disabled></el-input>
    </el-form-item>
    <el-form-item label="名称" prop="name">
      <el-input v-model="rowdata.name" placeholder="请输入名称"></el-input>
    </el-form-item>
    <el-form-item label="指派人" prop="action_user">
      <el-select v-model="rowdata.action_user" filterable multiple placeholder="请选择指派人">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="抄送人" prop="follow_user">
      <el-select v-model="rowdata.follow_user" filterable multiple placeholder="请选择跟踪人">
        <el-option v-for="item in users" :key="item.id" :value="item.username"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="需求人" prop="from_user">
      <el-input v-model="rowdata.from_user" placeholder="请输入需求人"></el-input>
    </el-form-item>
    <el-form-item label="类型" prop="type">
      <el-select v-model="rowdata.type" placeholder="请选择类型">
        <el-option v-for="item in types" :key="item.id" :value="item.name"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="内容" prop="content">
      <mavon-editor style="z-index: 1" v-model="rowdata.content" code_style="monokai"
                    :toolbars="toolbars" @imgAdd="imgAdd" ref="md"></mavon-editor>
      <a class="tips"> Tip：截图可以直接 Ctrl + v 粘贴到内容里面</a>
    </el-form-item>
    <el-form-item label="等级" prop="level">
      <el-rate
        v-model="rowdata.level"
        :colors="['#99A9BF', '#F7BA2A', '#ff1425']"
        show-text
        :texts="['E', 'D', 'C', 'B', 'A']">
      </el-rate>
      <a class="tips">Tip：星数代表问题紧急程度，星数越多，代表越紧急</a>
    </el-form-item>
    <el-form-item label="是否公开" prop="is_public">
      <el-switch v-model="rowdata.is_public" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
    </el-form-item>
    <el-form-item label="附件">
      <el-upload
        ref="upload"
        :action="uploadurl"
        :on-success="handleSuccess">
        <el-button slot="trigger" size="mini" type="success" plain>
          上传
        </el-button>
        <div slot="tip" class="el-upload__tip">
          <p><a style="color: red">最多只能上传5个文件</a></p>
        </div>
      </el-upload>
      <hr class="heng"/>
      <div v-if='enclosureData.length>0' class="ticketenclosure">
        <ul>
          <li v-for="item in enclosureData" :key="item.id" v-if="item.file" style="list-style:none">
            <i class="fa fa-paperclip"></i>
            <a :href="apiurl + '/upload/' + item.file" :download="item.file">{{item.file.split('/')[1]}}</a>
            <el-tooltip class="item" effect="dark" content="删除附件" placement="right">
              <el-button type="text" icon="el-icon-delete" @click="deleteEnclosure(item.id)"></el-button>
            </el-tooltip>
          </li>
        </ul>
      </div>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('rowdata')">更新</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { putProject, getProjectType } from '@/api/project'
import { postProjectEnclosure, deleteProjectEnclosure } from '@/api/project'
import { postUpload } from 'api/tool'
import { getUser } from 'api/user'
import { apiUrl, uploadurl } from '@/config'
import { getConversionTime, getCreatetime, getCreatedate } from '@/utils'

export default {
  components: {},

  props: ['rowdata', 'enclosureData'],
  data() {
    return {
      route_path: this.$route.path.split('/'),
      rules: {
        name: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        content: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请输入正确的内容', trigger: 'blur' }
        ]
      },
      users: [],
      toolbars: {
        preview: true, // 预览
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        ol: true, // 有序列表
        help: true
      },
      apiurl: apiUrl,
      uploadurl: uploadurl,
      types: [],
      img_file: {},
      enclosureForm: {
        project: this.rowdata.id,
        create_user: localStorage.getItem('username'),
        file: ''
      },
      fileList: []
    }
  },

  created() {
    this.getUsers()
    this.getTypes()
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.rowdata.update_date = getCreatedate()
          this.rowdata.update_time = getCreatetime()
          putProject(this.rowdata.id, this.rowdata).then(response => {
            if (response.statusText === '"Created"') {
              this.$message({
                type: 'success',
                message: '恭喜你，更新成功'
              })
            }
            this.$emit('DialogStatus', false)
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

    getTypes() {
      getProjectType().then(response => {
        this.types = response.data
      })
    },
    imgAdd(pos, file) {
      var md = this.$refs.md
      const formData = new FormData()
      formData.append('username', localStorage.getItem('username'))
      formData.append('file', file)
      formData.append('create_time', getConversionTime(file.lastModified))
      formData.append('type', file.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        md.$imglst2Url([[pos, response.data.file]])
      })
    },
    deleteEnclosure(id) {
      deleteProjectEnclosure(id).then(() => {
        this.$emit('UpdateEnclosure')
      })
    },
    handleSuccess(file, fileList) {
      const formData = new FormData()
      formData.append('username', this.enclosureForm.create_user)
      formData.append('file', fileList.raw)
      formData.append('create_time', getConversionTime())
      formData.append('type', fileList.raw.type)
      formData.append('archive', this.route_path[1])
      postUpload(formData).then(response => {
        this.enclosureForm.file = response.data.filepath
        postProjectEnclosure(this.enclosureForm)
        if (response.statusText === 'Created') {
          this.$message({
            type: 'success',
            message: '恭喜你，上传成功'
          })
        }
        this.$refs.upload.clearFiles() // 上传成功后清除上传列表
        this.$emit('UpdateEnclosure')
      }).catch(error => {
        this.$message.error('上传失败')
        this.$refs.upload.clearFiles()
        console.log(error)
      })
    }
  }
}
</script>

<style lang='scss'>
</style>

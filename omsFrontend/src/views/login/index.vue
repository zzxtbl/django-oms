<template>
  <div class="login-container">
    <el-form class="card-box login-form" autoComplete="on" :model="loginForm" ref="loginForm"
             label-position="left">
      <h3 class="title">Ojbk运维管理系统</h3>

      <el-form-item prop="username">
        <span class="svg-container svg-container_login">
          <icon name="user"></icon>
        </span>
        <el-input name="username" type="text" v-model="loginForm.username" autoComplete="on"
                  placeholder="用户名"></el-input>
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container"> <icon name="key"></icon></span>
        <el-input name="password" :type="pwdType" @keyup.enter.native="handleLogin" v-model="loginForm.password"
                  autoComplete="on" placeholder="密码">
          <span class="svg-container" slot="suffix" @click="showPwd"><icon :name="eye"></icon></span>
        </el-input>
      </el-form-item>
      <el-button type="primary" class="login-button" :loading="loading" @click.native.prevent="handleLogin">Login
      </el-button>
    </el-form>

    <el-tooltip effect="dark" content="切换背景" placement="top">
      <el-button class="qie" type="primary" size="mini" icon="el-icon-refresh" @click="changeBg"></el-button>
    </el-tooltip>
  </div>
</template>

<script>
export default {
  name: 'login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      pwdType: 'password',
      eye: 'eye',
      loading: false,
      showDialog: false,
      bgindex: 0
    }
  },
  methods: {
    showPwd() {
      if (this.pwdType === 'password') {
        this.pwdType = ''
        this.eye = 'eye-slash'
      } else {
        this.pwdType = 'password'
        this.eye = 'eye'
      }
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('Login', this.loginForm).then(() => {
            this.loading = false
            this.$router.push(this.$route.query.redirect || '/')
          }).catch(error => {
            const errordata = JSON.stringify(error.response.data)
            this.$message.error(errordata)
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    changeBg() {
      const image_list = [
        'http://pic1.win4000.com/wallpaper/2/582687f045785.jpg',
        'http://pic1.win4000.com/wallpaper/2/582687feb0f49.jpg',
        'http://pic1.win4000.com/wallpaper/d/584e538de8003.jpg',
        'http://pic1.win4000.com/wallpaper/9/5854ebc3ae1a7.jpg',
        'http://pic1.win4000.com/wallpaper/2/582687fb30871.jpg',
        'http://cdn2.wallpapersok.com/uploads/picture/877/63877/velikobritaniya-angliya-norfolk-7684.jpg'
      ]
      document.getElementsByClassName('login-container')[0].style.background = 'url(' + image_list[this.bgindex] + ')'
      if (this.bgindex < image_list.length - 1) {
        this.bgindex += 1
      } else {
        this.bgindex = 0
      }
    }
  },
  created() {
    // window.addEventListener('hashchange', this.afterQRScan)
  },
  destroyed() {
    // window.removeEventListener('hashchange', this.afterQRScan)
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  @import "src/styles/mixin.scss";

  $bg: #2d3a4b;
  $dark_gray: #889aa4;
  $light_gray: #d1eec4;

  .login-container {
    @include relative;
    background: url('../../assets/bg-images/bg0.jpg');
    // background-color: $bg;
    width: 100%;
    // background-size: 100% 100%;
    input:-webkit-autofill {
      -webkit-box-shadow: 0 0 0px 1000px #293444 inset !important;
      -webkit-text-fill-color: #fff !important;
    }
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
    }
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
    }
    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;
    }
    .svg-container {
      padding: 6px 5px 6px 15px;
      color: $dark_gray;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
      &_login {
        font-size: 20px;
      }
    }
    .title {
      font-size: 28px;
      font-weight: 500;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
    }
    .login-form {
      position: absolute;
      left: 0;
      right: 0;
      width: 400px;
      padding: 35px 35px 15px 35px;
      margin: 120px auto;
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
    .show-pwd {
      position: absolute;
      right: 10px;
      top: 7px;
      font-size: 16px;
      color: $dark_gray;
      cursor: pointer;
      user-select: none;
    }
    .login-button {
      width: 100%;
      background-color: #7cb3d2;
      border-color: #a8cae3;
    }
    .qie {
      position: absolute;
      right: 0;
      bottom: 0;
      background: transparent;
      border: none;
    }
  }
</style>

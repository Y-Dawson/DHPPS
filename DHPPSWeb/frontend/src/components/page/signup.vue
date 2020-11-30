<template>
  <div id="signup">
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
      <el-form :model="signupForm" :rules="signupFormRules" ref="signupForm" class="ms-content" action="">
      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="username"  style="margin-bottom: 15px;">
            <el-form-item prop="username">
              <el-input
                v-model="signupForm.username"
                placeholder="用户名"
                id="username"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="password" style="margin-bottom: 15px;">
            <el-form-item prop="password">
              <el-input
                v-model="signupForm.password"
                placeholder="输入密码"
                type="password"
                id="password"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="password2" style="margin-bottom: 15px;">
            <el-form-item prop="password2">
              <el-input
                v-model="signupForm.password2"
                placeholder="确认密码"
                type="password"
                id="password2"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="email" style="margin-bottom: 15px;">
            <el-form-item prop="email">
              <el-input
                v-model="signupForm.email"
                placeholder="邮箱"
                id="email"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="phone" style="margin-bottom: 15px;">
            <el-form-item prop="phone">
              <el-input
                v-model="signupForm.phone"
                placeholder="11位手机号"
                id="phonenum"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="securitt_code" style="margin-bottom: 15px;">
            <el-form-item prop="securitt_code">
              <el-input
                v-model="signupForm.securitt_code"
                placeholder="请输入验证码"
                id="securitt_code"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>

        <el-form-item>
          <el-button type="info" >获取验证码</el-button>
        </el-form-item>
      </div>

      <div class="layui-form-item">
        <el-form-item>
          <el-button type="primary" @click="submitForm('signupForm')">确认</el-button>
        </el-form-item>
      </div>
      <div class="layui-form-item">
        <el-form-item>
          <router-link class="use-account" to='/Login'>使用已有账号登录</router-link>
        </el-form-item>
      </div>
     </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    var checkanme= (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入昵称'));
        }
        setTimeout(() => {
          let reg =  /^[(a-zA-Z0-9\u4e00-\u9fa5){1}_#]{4,20}$/
          if (value == '' || !reg.test(value)) {
            callback(new Error('昵称限16个字符，支持中英文、数字、减号或下划线'));
          }
          else{
            callback();
          }
        });
      }
    // var validatePass= (rule, value, callback) => {
    //     if (!value) {
    //       return callback(new Error('请输入密码'));
    //     }
    //     setTimeout(() => {
    //       let reg =  /^[(a-zA-Z0-9\u4e00-\u9fa5){1}_#]{4,20}$/
    //       if (value == '' || !reg.test(value)) {
    //         callback(new Error('昵称限16个字符，支持中英文、数字、减号或下划线'));
    //       }
    //       else{
    //         callback();
    //       }
    //     });
    //   }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.signupForm.password) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    var checkphone = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入手机号'));
        }
        setTimeout(() => {
          let reg = /^1[0-9]{10}$/
          if (value == '' || value.length < 11 || !reg.test(value)) {
            callback(new Error('请输入正确的手机号'));
          }
          else{
            callback();
          }
        });
      };
    var checkemail=(rule, value, callback) =>{
        if(!value){
          return callback(new Error('请输入邮箱'));
        }
        setTimeout(()=>{
          let reg=/^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
          if(value==''||!reg.test(value)){
            callback(new Error('请输入正确的邮箱'));
          }
          else{
            callback();
          }
        });
      };
    return {
      signupForm: {
        username: "",
        password: "",
        password2: "",
        email:"",
        phone: "",
        securitt_code: "",
      },
      returnmessage:"",
      signupFormRules: {
        username: [
          { required: true, validator:checkanme , trigger: "blur"},
          { min: 3, max: 15, message: "长度在3到15个字符之间", trigger: "blur"}
          ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur"},
          { min: 6, max: 12, message: "长度在6到12个字符之间", trigger: "blur"}          ],
        password2: [
          { required: true, message: "请再次输入密码", trigger: "blur"},
          // { min: 6, max: 12, message: "长度在6到12个字符之间", trigger: "blur"},
          { validator: validatePass2, trigger: 'blur', required: true }
          ],
        email: [
          { required: true, validator:checkemail, trigger: "blur"},
          { min: 7, max: 20, message: "请输入正确的邮箱", trigger: "blur"}
          ],
        phone: [
          { required: true, validator:checkphone, trigger: "blur"},
          { min: 11, max: 11, message: "请输入11位手机号", trigger: "blur"}
          ],
        securitt_code: [
          { required: true, message: "请输入验证码", trigger: "blur"},
          { min: 4, max: 4, message: "请输入4位验证码", trigger: "blur"}
          ],
      }
    };
  },
  methods:{
    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.putContent()
            alert('submit!')
          } else {
            console.log('error submit!!')
            return false
          }
        });
      },
    postAccount: function () {
      var self = this;
      var self = this;
      let data = new FormData();
      data.append("username",$("#username").val());
      data.append("phonenum",$("#phonenum").val());
      data.append("email",$("#email").val());
      data.append("password",$("#password").val());
      data.append("verifyCode",$("#securitt_code").val());
      axios
        .post('http://127.0.0.1:8000/backend/signup/', data)
        .then(response => (
          self.content = response.data,
          self.returnmessage=response.data.message,
          // alert(self.returnmessage),
          self.skip()
          // alert(JSON.stringify(response.data.message))
        ))
        .catch(function (error) {
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.postAccount()
        } else {
          console.log('error submit!!')
          return false
        }
      });
    },
    skip() {
      if(this.returnmessage=="注册成功") {
        this.$router.push({path:'/Login'});
      }
      else this.$message(this.returnmessage);
    }
  }
};
</script>
<style>
@import "../../assets/layui/css/layui.css";
body {
  background-image: url(../../assets/img/background2.jpg);
  /* width: 1000px; */
}
</style>
<style scoped>
@import "../../assets/layui/css/layui.css";
.ms-login {
    position: absolute;
    left: 50%;
    top: 35%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.5);
    overflow: hidden;
}
.ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #fff;
    border-bottom: 1px solid #ddd;
}
.ms-content {
  text-align: center;
  margin: 0;
  padding: 30px 30px;
}


.layui-form input {
  width: 300px;
  height: 40px;
}

.layui-form .layui-input-inline {
  margin: 0;
}

.layui-form .layui-form-item {
  text-align: center;
}

.layui-form-item a {
  font-size: 10px;
}

.account input.el-input__inner,
.password input.el-input__inner {
  border-radius: 0px 5px 5px 0px;
}

.btns {
  display: flex;
  justify-content: center;
}

.layui-form * {
  margin: 0;
}

.layui-form-item .layui-input-block {
  margin-bottom: 20px;
}

.get-verification {
  margin-left: -25px;
  background-color: #fff;
  font-size: 16px;
  border-radius: 10px;
}

.username input.el-input__inner,
.password input.el-input__inner,
.password2 input.el-input__inner,
.phone input.el-input__inner,
.securitt_code input.el-input__inner {
  border-radius: 30px;
}

.securitt_code input.el-input__inner {
  margin-left: -150px;
  width: 250px;
}

.el-button--info {
  position: absolute;
  width: 80px;
  height: 35px;
  margin-left: 32px;
  margin-top: -57px;
}

.el-button--primary {
  position: absolute;
  width: 125px;
  height: 30px;
  margin-left: -65px;
}

.use-account {
  position: absolute;
  margin-top: 10px;
  margin-left: -60px;
}
</style>
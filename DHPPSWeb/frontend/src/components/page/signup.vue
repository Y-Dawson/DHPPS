<template>
  <div id="signup">
    <div
      class="logo"
      style="text-align: center; margin-top: 80px; margin-bottom: 30px"
    >
      <i
        class="layui-icon layui-icon-windows"
        style="font-size: 100px; color: #1e9fff"
      ></i>
    </div>

    <el-form
      :model="signupForm"
      :rules="signupFormRules"
      ref="signupForm"
      class="layui-form"
      action=""
    >
      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="username"  style="margin-bottom: 15px;">
            <el-form-item prop="username">
              <el-input
                v-model="signupForm.username"
                placeholder="用户名"
                id="username"
              ></el-input>
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
              ></el-input>
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
              ></el-input>
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
              ></el-input>
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
              ></el-input>
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
              ></el-input>
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

        <el-form-item>
          <router-link class="use-account" to='/Login'>使用已有账号登录</router-link>
        </el-form-item>
      </div>
    </el-form>
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
          self.returnData = response.data,
          // alert(JSON.stringify(response)),
          alert(JSON.stringify(response.data.message))
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
  }
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";

body {
  background-color: pink;
  /* width: 1000px; */
}

.layui-form * {
  margin: 0;
}

.layui-form input {
  width: 400px;
  height: 48px;
}

.layui-form .layui-input-inline {
  margin: 0;
}

.layui-form .layui-form-item {
  text-align: center;
}

.layui-form-item a {
  font-size: 12px;
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
  width: 125px;
  height: 30px;
  margin-left: 110px;
  margin-top: -55px;
}

.el-button--primary {
  position: absolute;
  width: 125px;
  height: 30px;
  margin-left: -65px;
}

.use-account {
  position: absolute;
  margin-left: 75px;
}
</style>
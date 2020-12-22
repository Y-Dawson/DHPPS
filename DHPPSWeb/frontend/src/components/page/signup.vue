<template>
  <div id="signup">
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
      <el-form
        :model="signupForm"
        :rules="signupFormRules"
        ref="signupForm"
        class="ms-content"
        action=""
      >
        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="username" style="margin-bottom: 15px">
              <el-form-item prop="username">
                <el-input
                  v-model="signupForm.username"
                  placeholder="用户名"
                  id="username"
                  class="MyInput"
                >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="password" style="margin-bottom: 15px">
              <el-form-item prop="password">
                <el-input
                  v-model="signupForm.password"
                  placeholder="输入密码"
                  type="password"
                  id="password"
                  class="MyInput"
                >
                <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="password2" style="margin-bottom: 15px">
              <el-form-item prop="password2">
                <el-input
                  v-model="signupForm.password2"
                  placeholder="确认密码"
                  type="password"
                  id="password2"
                  class="MyInput"
                >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="email" style="margin-bottom: 15px">
              <el-form-item prop="email">
                <el-input
                  v-model="signupForm.email"
                  placeholder="邮箱"
                  id="email"
                  class="MyInput"
                >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="phone" style="margin-bottom: 15px">
              <el-form-item prop="phone">
                <el-input
                  v-model="signupForm.phone"
                  placeholder="11位手机号"
                  id="phonenum"
                  class="MyInput"
                >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="layui-form-item">
          <div class="layui-inline">
            <div class="securitt_code" style="margin-bottom: 15px">
              <el-form-item prop="securitt_code">
                <el-input
                  v-model="signupForm.securitt_code"
                  placeholder="请输入验证码"
                  id="securitt_code"
                  class="MyInput"
                >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                </el-input>
              </el-form-item>
            </div>
          </div>

          <el-form-item>
            <el-button type="info" :disabled="disabled" @click="checkPhone()">{{valiBtn}}</el-button>
          </el-form-item>
        </div>

        <div class="layui-form-item">
          <el-form-item>
            <el-button type="primary" @click="submitForm('signupForm')"
              >确认</el-button
            >
          </el-form-item>
        </div>
        <div class="layui-form-item">
          <el-form-item >
            <router-link class="use-account" to="/Login" style="color:#fff;margin-top:20px;"
              >使用已有账号登录</router-link
            >
          </el-form-item>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    var checkanme = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入昵称"));
      }
      setTimeout(() => {
        let reg = /^[(a-zA-Z0-9\u4e00-\u9fa5){1}_#]{1,20}$/;
        if (value == "" || !reg.test(value)) {
          callback(new Error("昵称限20个字符，支持中英文、数字或下划线"));
        } else {
          callback();
        }
      });
    };
    var validatePass = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入密码"));
      }
      setTimeout(() => {
        let reg = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[._~!@#$^&*])[A-Za-z0-9._~!@#$^&*]{6,12}$/;
        if (value == "" || !reg.test(value)) {
          callback(
            new Error(
              "密码长度为6~12位，必须由字母、数字、特殊符号(._~!@#$^&*)组成"
            )
          );
        } else {
          callback();
        }
      });
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.signupForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    var checkphone = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入手机号"));
      }
      setTimeout(() => {
        let reg = /^1[0-9]{10}$/;
        if (value == "" || value.length < 11 || !reg.test(value)) {
          callback(new Error("请输入正确的手机号"));
        } else {
          callback();
        }
      });
    };
    var checkemail = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("请输入邮箱"));
      }
      setTimeout(() => {
        let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        if (value == "" || !reg.test(value)) {
          callback(new Error("请输入正确的邮箱"));
        } else {
          callback();
        }
      });
    };
    return {
      valiBtn: "获取验证码",
      disabled: false,
      signupForm: {
        username: "",
        password: "",
        password2: "",
        email: "",
        phone: "",
        securitt_code: "",
      },
      returnmessage: "",
      signupFormRules: {
        username: [{ required: true, validator: checkanme, trigger: "blur" }],
        password: [
          { required: true, validator: validatePass, trigger: "blur" },
        ],
        password2: [
          { validator: validatePass2, trigger: "blur", required: true },
        ],
        email: [
          { required: true, validator: checkemail, trigger: "blur" },
          { min: 7, max: 20, message: "请输入正确的邮箱", trigger: "blur" },
        ],
        phone: [
          { required: true, validator: checkphone, trigger: "blur" },
          { min: 11, max: 11, message: "请输入11位手机号", trigger: "blur" },
        ],
        securitt_code: [
          { required: true, message: "请输入验证码", trigger: "blur" },
          { min: 6, max: 6, message: "请输入6位验证码", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    checkPhone: function () {
      this.$refs["signupForm"].validateField("phone", (err) => {
        if (err) {
          console.log("未通过");
          return;
        } else {
          console.log("已通过");
          this.getVerifyCode();
        }
      });
    },
    tackBtn: function () {
      let time = 60;
      let timer = setInterval(() => {
        if (time == 0) {
          clearInterval(timer);
          this.valiBtn = "获取验证码";
          this.disabled = false;
        } else {
          this.disabled = true;
          this.valiBtn = time + "秒后重试";
          time--;
        }
      }, 1000);
    },
    phoneIsValid: function() {
      if(this.returnmessage=="验证码已发送") {
            this.$message(this.returnmessage);
            this.tackBtn(); //验证码倒数60秒
          }
          else this.$message(this.returnmessage);
    },
    getVerifyCode: function () {
      var self = this;
      let data = new FormData();
        data.append("phoneNum", $("#phonenum").val());
      axios
        .post("/apis/backend/requestSmsCode/", data)
        .then(
          (response) => (
            (self.content = response.data),
            self.returnmessage=response.data.message,
            self.phoneIsValid()            
            // alert(self.returnmessage),
            // self.skip()
            // alert(JSON.stringify(response.data.message))
          )
        )
        .catch(function (error) {
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    postAccount: function () {
      var self = this;
      let data = new FormData();
      data.append("userName", $("#username").val());
      data.append("phoneNum", $("#phonenum").val());
      data.append("email", $("#email").val());
      data.append("password", $("#password").val());
      data.append("verifyCode", $("#securitt_code").val());

      axios
        .post("/apis/backend/signup/", data)
        .then(
          (response) => (
            (self.content = response.data),
            (self.returnmessage = response.data.message),
            // alert(self.returnmessage),
            self.skip()
            // alert(JSON.stringify(response.data.message))
          )
        )
        .catch(function (error) {
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.postAccount();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    skip() {
      if (this.returnmessage == "注册成功") {
        this.$message(this.returnmessage);
        this.$router.push({ path: "/Login" });
      } else this.$message(this.returnmessage);
    },
  },
};
</script>
<style>
.MyInput .el-input__inner{
  background-color: transparent;
  border-radius: 0px;
  border:0px;
  border-bottom: 1px white solid;
  color: #fff;
}
.MyInput .el-input__inner:hover{
  background-color: transparent;
  border-radius: 0px;
  border:0px;
  border-bottom: 1px white solid;
}
.MyInput .el-input__inner:focus-within{
  background-color: transparent;
  border-radius: 0px;
  border:0px;
  border-bottom: 1px white solid;
}
</style>
<style scoped>
@import "../../assets/layui/css/layui.css";
#signup{
  width: 100%;
  height: 100%;
  background-image: url(../../assets/img/3.jpg);
  background-size: cover;
  position: absolute;
  z-index: -1;
  background-repeat: no-repeat;
}
.ms-login {
    position: absolute;
    left: 50%;
    top: 35%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(24, 26, 37, 0.5);
    overflow: hidden;
    padding-bottom: 10px;
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

.layui-form .layui-form-item {
  text-align: center;
}

.el-button--info {
  position: absolute;
  width: 80px;
  height: 32px;
  margin-left: 25px;
  margin-top: -60px;
  background-color: transparent;
}

.el-button--primary {
  position: absolute;
  width: 125px;
  height: 30px;
  margin-left: -65px;
  background-color: #5D5EB4;
  border:0px;
}

.use-account {
  position: absolute;
  margin-top: 10px;
  margin-left: -60px;
}
</style>
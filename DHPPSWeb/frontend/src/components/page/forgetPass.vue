<template>
  <div id="ForgetPass">
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
      <el-form :model="forgetForm" :rules="forgetFormRules" ref="forgetForm" class="ms-content" action="">
      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="phone">
            <el-form-item prop="phone">
              <el-input
                v-model="forgetForm.phone"
                placeholder="请输入11位手机号"
                id="phone"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="securitt_code">
            <el-form-item prop="securitt_code">
              <el-input
                v-model="forgetForm.securitt_code"
                placeholder="请输入验证码"
                id="securitt_code"
              >
              <el-button slot="prepend" icon="el-icon-user"></el-button>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="info" >获取验证码</el-button>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="password">
            <el-form-item prop="password">
              <el-input
                v-model="forgetForm.password"
                placeholder="请填写6到12位密码"
                type="password"
                id="password"
              >
              <el-button slot="prepend" icon="el-icon-lock"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="password2">
            <el-form-item prop="password2">
              <el-input
                v-model="forgetForm.password2"
                placeholder="确认密码"
                type="password"
                id="password2"
              >
              <el-button slot="prepend" icon="el-icon-lock"></el-button>
              </el-input>
            </el-form-item>
          </div>
        </div>
      </div>
      <el-form-item class="btns">
        <router-link to='/Login'><el-button type="return" >返 回</el-button></router-link>
        <el-button type="primary" @click="SubmitForm('forgetForm')">确 定</el-button>
      </el-form-item>
     </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    var validatePass= (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入密码'));
        }
        setTimeout(() => {
          let reg =  /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[._~!@#$^&*])[A-Za-z0-9._~!@#$^&*]{6,12}$/
          if (value == '' || !reg.test(value)) {
            callback(new Error('密码长度为6~12位，必须由字母、数字、特殊符号(._~!@#$^&*)组成'));
          }
          else{
            callback();
          }
        });
      }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.forgetForm.password) {
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
    return {
      forgetForm: {
        password: "",
        password2: "",
        phone: "",
        securitt_code: ""
      },
      returnData:[],
      returnmessage:"",
      forgetFormRules: {
        password: [{ required: true, validator:validatePass,trigger: "blur"}],
        password2: [{ validator: validatePass2, trigger: 'blur', required: true }],
        phone: [{ required: true, validator:checkphone, trigger: "blur"}],
        securitt_code: [
          { required: true, message: "请输入验证码", trigger: "blur"},
          { min: 4, max: 4, message: "请输入4位验证码", trigger: "blur"}
          ],
      }
    };
  },
  methods:{
    ForgetPass: function () {
      var self = this;
      let data = new FormData();
      data.append("phonenum",$("#phone").val());
      data.append("verifyCode",$("#securitt_code").val());
      data.append("newPassword",$("#password").val());
      axios
        .post('http://127.0.0.1:8000/backend/forgetPwd/', data)
        .then(response => (
          self.returnData = response.data,
          self.returnmessage=response.data.message,
          self.Skip()
        ))
        .catch(function (error) {
          alert(JSON.stringify(error.response));
          console.log(error.response);
        });
    },
    SubmitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.ForgetPass()
        } else {
          console.log('error submit!!')
          return false
        }
      });
    },
    Skip() {
      if(this.returnmessage=="修改成功") {
        this.$message(this.returnmessage);
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
}
</style>

<style scoped>
@import "../../assets/layui/css/layui.css";
.ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    height:380px;
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
.layui-form .layui-form-item {
  text-align: center;
}
.el-button--info {
  position: absolute;
  width: 80px;
  height: 35px;
  margin-left: 36px;
  margin-top: -38px;
}
.el-button--return {
  position: absolute;
  width: 100px;
  height: 40px;
  margin-left: -120px;
}
.el-button--primary{
  position: absolute;
  width: 100px;
  height: 40px;
  margin-left: 10px;
}
</style>

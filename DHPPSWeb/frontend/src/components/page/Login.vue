<template>
  <div calss="login" :style="bgImg" >
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
        <el-form :model="loginForm" :rules="loginFormRules" ref="loginFormRef" class="ms-content" action="">
              <div class="account">
                <el-form-item prop="account">
                  <el-input
                    v-model="loginForm.account"
                    placeholder="用户名/密码"
                    id="loginPhone"
                  >
                  <el-button slot="prepend" icon="el-icon-user"></el-button>
                  </el-input>
                </el-form-item>
              </div>

              <div class="password">
                <el-form-item prop="password">
                  <el-input
                    v-model="loginForm.password"
                    placeholder="请填写6到12位密码"
                    type="password"
                    id="loginPass"
                  >
                  <el-button slot="prepend" icon="el-icon-lock"></el-button>
                  </el-input>
                </el-form-item>
              </div>

      <el-form-item class="btns">
        <el-button type="primary" @click="login">登 录</el-button>
        <el-button type="info" @click="resetLoginForm">重 置</el-button>
      </el-form-item>
      <router-link to="/signup" class="create-account" style="margin-left:10px; float:left;">创建账号</router-link>
      <router-link to="/forgetPass" class="forget-password" style="margin-left:10px; float:right;">忘记密码</router-link>
      <!-- <a class="forget-password" href="./forgetPass" style="margin-right:10px; float:right;">忘记密码</a> -->
     </el-form>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      bgImg:{ backgroundImage:"url(" + require("../../assets/img/background2.jpg") + ")",
              height:'100vh',//这里一定要设置高度 否则背景图无法显示
              backgroundRepeat: "no-repeat"},
      loginMassege:'',
      loginForm: {
      account: "",
      password: "",
      },

      loginFormRules: {
        account: [
          { required: true, message: "请输入用户名/手机号", trigger: "blur" },
          {
            min:11, max:11,
            message: "请输入正确的手机号",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 12,
            message: "请输入正确的密码（长度在6到12个字符之间）",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    submitMessage(){
      if(this.loginMassege=="登录成功"){
        // this.$cookies.get(keyName)
        // alert(this.$cookies.get(sessionid))
        this.$message.success("登录成功！");
        this.$router.push({path:'/Setting'});
      }
      else{
        if(this.loginMassege=="密码错误"){
          this.$message.error("密码错误")
        }
        else{
          this.$message.error("账号不存在")
        }
      }
    
    },
    resetLoginForm() {
      this.$refs.loginFormRef.resetFields();
    },
    getLoginData: function () {
      var self = this
      axios
        .get("http://127.0.0.1:8000/backend/logindata/")
        .then(response => (
            self.content = response.data
            // alert(JSON.stringify(response))
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(response));
          alert("数据获取失败");
          console.log(error.response);
        });
    },
    postContent: function () {
      var self = this
      let data = new FormData()
      data.append("phonenum",$("#loginPhone").val())
      data.append("password",$("#loginPass").val())
      axios
        .post("http://127.0.0.1:8000/backend/signin/",data)
        .then(response => (
            self.content = response.data,
            self.loginMassege=response.data.message,
            alert("数据发送"),
            // alert(JSON.stringify(self.loginMassege)),
            self.submitMessage()
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    login() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (!valid) return
        this.postContent()
      });
    },
  },
};
</script>

<style>
@import "../../assets/layui/css/layui.css";
 /* body {
  background-image: url(../../assets/img/background2.jpg)
} */
.ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
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


.account input.el-input__inner,
.password input.el-input__inner {
  border-radius: 0px 5px 5px 0px;
}
.el-input{
  width: 270px;
  height: 20px;
}
.btns {
  display: flex;
  justify-content: center;
}

.el-button--primary,
.el-button--info {
  width: 100px;
}
</style>

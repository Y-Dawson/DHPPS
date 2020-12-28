<template>
  <div class="login" >
    <!-- <vue-particles
        color="#fff"
        :particleOpacity="0.7"
        :particlesNumber="60"
        shapeType="star"
        :particleSize="4"
        linesColor="#fff"
        :linesWidth="1"
        :lineLinked="true"
        :lineOpacity="0.4"
        :linesDistance="150"
        :moveSpeed="2"
        :hoverEffect="true"
        hoverMode="grab"
        :clickEffect="true"
        clickMode="push"
      >
      </vue-particles> -->
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
        <el-form :model="loginForm" :rules="loginFormRules" ref="loginFormRef" class="ms-content" action="">
              <div class="account">
                <el-form-item prop="account" class="loginForm">
                  <el-input
                    v-model="loginForm.account"
                    placeholder="用户名/手机号"
                    id="loginPhone"
                    clearable
                    class="MyInput"
                  >
                  <i slot="prefix" class="el-input__icon el-icon-user"></i>
                  </el-input>
                </el-form-item>
              </div>

              <div class="password">
                <el-form-item prop="password" class="loginForm">
                  <el-input
                    v-model="loginForm.password"
                    placeholder="请填写6到12位密码"
                    type="password"
                    id="loginPass"
                    class="MyInput"
                  >
                  <i slot="prefix" class="el-input__icon el-icon-lock"></i>
                  </el-input>
                </el-form-item>
              </div>

      <el-form-item class="btns">
        <el-button type="primary" @click="login">登 录</el-button>
        <el-button type="info" @click="resetLoginForm">重 置</el-button>
      </el-form-item>
      <router-link to="/signup" class="create-account">创建账号</router-link>
      <router-link to="/forgetPass" class="forget-password" style="font-size:14px;margin-left:10px; float:right;">忘记密码</router-link>
      <!-- <a class="forget-password" href="./forgetPass" style="margin-right:10px; float:right;">忘记密码</a> -->
     </el-form>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      ifLogin:'',
      loginMassege:'',
      userId:'',
      userAuthority:"",
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
  mounted:function(){
    this.GetUserIdentity();
    // this.JumpPage();
  },
  methods: {
    submitMessage(){
      if(this.loginMassege=="登录成功"){
        // this.$cookies.get(keyName)
        // alert(this.$cookies.get(sessionid))
        this.$message.success("登录成功！");
        if(this.userAuthority=="普通用户"){
          this.$router.push({
            path:'/setting',
            query:{
              params:JSON.stringify({
                userId:this.userId,
                caseName: 999,
                userAuthority:this.userAuthority
              })
            },
          });
        }
        else if(this.userAuthority=="管理员"){
          this.$router.push({
            path:'/AdminIndex',
            query:{
              params:JSON.stringify({
                userId:this.userId,
                userAuthority:this.userAuthority
              })
            },
          });
        }
        else if(this.userAuthority=="超级管理员"){
          this.$router.push({
            path:'/SuperIndex',
            query:{
              params:JSON.stringify({
                userId:this.userId,
                userAuthority:this.userAuthority
              })
            },
          });
        }
      }
      else{
        // if(this.loginMassege=="你已经登录"){
        // this.$message("你已经登录")
        // this.$router.push({
        //     path:'/setting',
        //     query:{
        //       params:JSON.stringify({
        //         userId:this.userId,
        //         userAuthority:this.userAuthority
        //       })
        //     },
        //   });
        // }
        if(this.loginMassege=="密码错误"){
          this.$message.error("密码错误")
        }
        if(this.loginMassege=="账号不存在"){
          this.$message.error("账号不存在")
        }
      }
    
    },
    resetLoginForm() {
      this.$refs.loginFormRef.resetFields();
    },
    //获取用户登陆状态
    GetUserIdentity(){
      var self=this
      axios
        .post("/apis/backend/getIdentity/")
        .then(response => (
          //  alert(JSON.stringify(response)),
           self.userId=response.data.userId,
           self.ifLogin=response.data.message,
           self.JumpPage()
          //  alert(self.ifLogin)
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    //判断用户是否需要再次登陆
    JumpPage:function(){
      // alert(this.ifLogin)
      if(this.ifLogin=="返回数据成功"){
        this.$message("你已经登陆")
        this.$router.push({
            path:'/setting',
            query:{
              params:JSON.stringify({
                userId:this.userId,
                userAuthority:this.userAuthority,
                caseName: 999
              })
            },
          });
      }
    },
    postContent: function () {
      var self = this
      let data = new FormData()
      data.append("phoneNum",$("#loginPhone").val())
      data.append("password",$("#loginPass").val())
      axios
        .post("/apis/backend/signin/",data)
        .then(response => (
            self.content = response.data,
            self.loginMassege=response.data.message,
            self.userId=response.data.userId,
            self.userAuthority=response.data.userAuthority,
            // alert("数据发送"),
            alert(JSON.stringify(response.data.message)),
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
.login{
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
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(24, 26, 37, 0.5);
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


.loginForm {
  border-radius: 0px 5px 5px 0px;
  padding-bottom: 20px;
}
.el-input{
  width: 270px;
  height: 20px;
  font-size: 12px;
}
.create-account{
  font-size:14px;
  font-weight: lighter;
  margin: 10px;
  float:left;
  color: #fff;
}
.forget-password{
  font-size:14px;
  font-weight: lighter;
  margin: 10px;
  float:right;
  color:#fff;
}
.btns {
  display: flex;
  justify-content: center;
}
.el-button--primary{
  background-color: #5D5EB4;
}
.el-button--primary,
.el-button--info {
  width: 100px;
  height: 35px;
  border: 0px;
}
</style>

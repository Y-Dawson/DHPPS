<template>
  <div id="login">
    <div
      class="logo"
      style="text-align: center; margin-top: 100px; margin-bottom: 50px"
    >
      <i
        class="layui-icon layui-icon-windows"
        style="font-size: 100px; color: rgb(247, 252, 252)"
      ></i>
    </div>

    <el-form
      :model="loginForm"
      :rules="loginFormRules"
      ref="loginFormRef"
      class="layui-form"
      action=""
    >
      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="account" style="margin-bottom: 20px">
            <el-form-item prop="account">
              <el-input
                v-model="loginForm.account"
                placeholder="用户名/密码"
                id="loginPhone"
              ></el-input>
            </el-form-item>
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div class="layui-inline">
          <div class="password" style="margin-bottom: 20px">
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                placeholder="请填写6到12位密码"
                type="password"
                id="loginPass"
              ></el-input>
            </el-form-item>
          </div>
          <!-- <div class="layui-form-mid layui-word-aux">请填写6到12位密码</div> -->
        </div>
      </div>

      <el-form-item class="btns">
        <el-button type="primary" @click="login">登 录</el-button>
        <el-button type="info" @click="resetLoginForm">重 置</el-button>
      </el-form-item>

      <div class="layui-form-item">
        <div class="layui-inline" style="margin-left: -330px">
          <label
            class="layui-form-label"
            style="font-size: 12px; margin-top: 2px; padding: 0 10px"
            >记住密码</label
          >
          <div class="layui-input-block" style="display: inline-block">
            <input
              type="checkbox"
              name="close"
              lay-skin="switch"
              lay-text="ON|OFF"
            />
          </div>
        </div>
      </div>

      <div class="layui-form-item">
        <div
          class="layui-input-block"
          style="
            position: absolute;
            display: inline-block;
            margin-top: -38px;
            margin-left: 150px;
          "
        >
          <a class="forget-password" href="#">忘记密码</a>
        </div>
      </div>

      <div class="layui-form-item">
        <div
          class="layui-input-block"
          style="position: absolute; display: inline-block; margin-left: -202px"
        >
          <router-link to="/signup" class="create-account">创建账号</router-link>
          <!-- <a class="create-account" href="./Signup">创建账号</a> -->
        </div>
      </div>

      <div class="layui-form-item">
        <div
          class="layui-input-block"
          style="position: absolute; display: inline-block; margin-left: 150px"
        >
          <!-- <a class="find-help" href="#">其他帮助</a> -->
        </div>
      </div>

      <div id="test"></div>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        account: "",
        password: "",
      },

      loginFormRules: {
        account: [
          { required: true, message: "请输入用户名/手机号", trigger: "blur" },
          {
            min: 3,
            max: 15,
            message: "长度在3到15个字符之间",
            trigger: "blur",
          },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          {
            min: 6,
            max: 12,
            message: "长度在6到12个字符之间",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    resetLoginForm() {
      this.$refs.loginFormRef.resetFields();
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
            alert("数据发送"),
            alert($("#loginPhone").val()),
            alert($("#loginPass").val()),
            alert(JSON.stringify(response))
          )
        )
        .catch(function (error) {
          alert(JSON.stringify(response));
          alert("数据发送失败");
          console.log(error.response);
        });
    },
    login() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (!valid) return;
        this.postContent();
        /*
      const { data: res }= await this.$http.post('app',this.loginForm);
      if(res.meta.status !== 200) return this.$message.error('登录失败！');
      */
        this.$message.success("登录成功！");
        window.sessionStorage.setItem("token", res.data.token);
        this.$router.push("./components/setting");
      });
    },
  },
};
</script>

<style>
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

.account input.el-input__inner,
.password input.el-input__inner {
  border-radius: 30px;
}

.btns {
  display: flex;
  justify-content: center;
}

.el-button--primary,
.el-button--info {
  width: 150px;
}
</style>

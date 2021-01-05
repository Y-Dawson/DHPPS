<template>
  <div class="login">
    <div class="ms-login">
      <div class="ms-title">高传染性疾病预测系统</div>
      <div class="ms-content" style="border-bottom: 1px solid #ddd">
        <div class="ms-content1">
          <div style="font-size: 20px; color: #fff; margin-top: 50px">
            自由模式
          </div>
          <!-- <div style="margin-top:10px;font-size: 20px; color: #fff">开始创建您的案例！</div> -->
          <el-button
            type="primary"
            @click="toSetting"
            style="margin-top: 50px; margin-bottom: 40px"
            >Start</el-button
          >
        </div>
        <img src="../../images/city.png" alt="" style="width: 35%;" />
        <!-- <div class="ms-content2">自由模式</div> -->
      </div>
      <div class="ms-content">
        <div class="ms-content1">
          <div style="font-size: 20px; color: #fff; margin-top: 50px">
            地图模式
          </div>
          <!-- <div style="margin-top:10px;font-size: 20px; color: #fff">开始创建您的案例！</div> -->
          <el-button
            type="primary"
            @click="toSettingMap"
            style="margin-top: 50px; margin-bottom: 40px"
            >Start</el-button
          >
        </div>
        <img src="../../images/Cmap.png" alt="" style="width: 50%" />
        <!-- <div class="ms-content2">自由模式</div> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ifLogin: '',
      loginMassege: '',
      userId: '',
      userAuthority: '',
      loginForm: {
        account: '',
        password: ''
      }
    }
  },
  mounted: function () {
  },
  methods: {
    toSetting: function() {
      this.$router.push({
        path: '/setting',
        query: {
          params: JSON.stringify({
            caseName: 999
          })
        }
      })
    },
    toSettingMap: function() {
      this.$router.push({
        path: '/settingMap',
        query: {
          params: JSON.stringify({
            caseName: 999
          })
        }
      })
    }
  }
}
// document.write(location.href);
</script>
<style>
.MyInput .el-input__inner {
  background-color: transparent;
  border-radius: 0px;
  border: 0px;
  border-bottom: 1px white solid;
  color: #fff;
}
.MyInput .el-input__inner:hover {
  background-color: transparent;
  border-radius: 0px;
  border: 0px;
  border-bottom: 1px white solid;
}
.MyInput .el-input__inner:focus-within {
  background-color: transparent;
  border-radius: 0px;
  border: 0px;
  border-bottom: 1px white solid;
}
</style>
<style scoped>
@import "../../assets/layui/css/layui.css";
.back {
  position: absolute;
  left: 47%;
  top: 70%;
  color: #fff;
  font-size: 14px;
  border: 1px #fff solid;
  padding: 10px;
  border-radius: 8px;
}
.login {
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
  left: 40%;
  top: 40%;
  width: 600px;
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
  width: 100%;
  padding: 1px;
  padding: 30px 30px;
  box-sizing: border-box;
}
.ms-content1 {
  width: 50%;
  text-align: center;
  float: left;
}
.ms-content2 {
  width: 50%;
  text-align: center;
}

.loginForm {
  border-radius: 0px 5px 5px 0px;
  padding-bottom: 20px;
}
.el-input {
  width: 270px;
  height: 20px;
  font-size: 12px;
}
.create-account {
  font-size: 14px;
  font-weight: lighter;
  margin: 10px;
  float: left;
  color: #fff;
}
.forget-password {
  font-size: 14px;
  font-weight: lighter;
  margin: 10px;
  float: right;
  color: #fff;
}
.btns {
  display: flex;
  justify-content: center;
}
.el-button--primary {
  background-color: #5d5eb4;
}
.el-button--primary,
.el-button--info {
  width: 100px;
  height: 35px;
  border: 0px;
}
</style>

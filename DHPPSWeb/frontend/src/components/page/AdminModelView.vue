<template>
  <div v-if="authorityShow" style="background-color: rgb(235, 234, 250)">
    <div class="wrapper">
      <!-- Sidebar  -->
      <div class="iq-sidebar" style="z-index: 1">
        <div class="iq-sidebar-logo d-flex justify-content-between">
          <span style="font-size: 18px">高传染性疾病预测系统</span>
        </div>
        <div id="sidebar-scrollbar">
          <nav class="iq-sidebar-menu">
            <ul class="iq-menu" style="margin-top: 20px">
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminIndex',
                  }"
                  ><i class="ri-home-4-line"></i><span>首页</span></router-link
                >
              </li>
              <!-- <li class="active">
                        <a href="javascript:void(0);" class="iq-waves-effect"><i class="ri-user-line"></i><span>User</span><i class="ri-arrow-right-s-line iq-arrow-right"></i></a>
                        <ul class="iq-submenu">
                           <li><a href="profile.html"><i class="ri-profile-line"></i>用户管理</a></li>
                           <li class="active"><a href="user-list.html"><i class="ri-file-list-line"></i>员工管理</a></li>
                        </ul>
                     </li> -->
              <li>
                <a class="iq-waves-effect" @click="adminOrSuperAdmin()"
                  ><i class="ri-user-line"></i><span>信息管理</span></a
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminCaseManage',
                  }"
                  ><i class="ri-home-4-line"></i
                  ><span>案例管理</span></router-link
                >
              </li>
              <li class="active">
                <a class="iq-waves-effect"
                  ><i class="ri-profile-line"></i>查看模型</a
                >
              </li>
            </ul>
          </nav>
          <div class="p-3"></div>
        </div>
      </div>
      <!-- TOP Nav Bar -->
      <div class="iq-top-navbar" style="z-index: 1">
        <div class="iq-navbar-custom">
          <nav class="navbar navbar-expand-lg navbar-light p-0">
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav ml-auto navbar-list">
                <li class="nav-item"></li>
              </ul>
            </div>
            <ul class="navbar-list">
              <li>
                <div class="chat-header-icons d-flex">
                  <router-link
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 100px; font-size: 14px; margin-top: 18px"
                    :to="{
                      path: '/UserProfile',
                    }"
                  >
                    <i class="ri-reply-fill"></i>
                    个人中心
                  </router-link>
                </div>
              </li>
              <li>
                <el-popover placement="bottom" width="400" trigger="click">
                  <el-calendar v-model="value"> </el-calendar>
                  <el-button slot="reference" id="calendar">
                    <i
                      class="ri-calendar-line"
                      style="font-size: 20px; color: rgb(135, 123, 244)"
                    ></i>
                  </el-button>
                </el-popover>
              </li>
              <li>
                <a class="d-flex align-items-center">
                  <img
                    :src="AdminUrl"
                    class="img-fluid rounded mr-3"
                    alt="user"
                  />
                  <div class="caption">
                    <h6 class="mb-0 line-height">{{ MyContent.userName }}</h6>
                  </div>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
      <!-- TOP Nav Bar END -->
      <!-- Page Content  -->
      <div id="content-page" class="content-page">
        <div class="container-fluid">
          
          <div class="row box animated bounceInRight" id="f" v-if="show" >
            <div class="col-sm-2 col-lg-12">
              <div
                class="iq-card"
              >
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">Convlution</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade1"
                  >
                    查看详情
                  </a>
                </div>
                </div>
                <div class="iq-card-body">在泛函分析中，卷积、旋积或摺积(英语：Convolution)是通过两个函数f和g 生成第三个函数的一种数学算子，表征函数f与g经过翻转和平移的重叠部分函数值乘积对重叠长度的积分。</div>
              </div>
            </div>
            <div class="col-sm-2 col-lg-12">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">ConvLSTM</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade2"
                  >
                    查看详情
                  </a>
                </div>
                </div>
                <div class="iq-card-body">LSTM在时序数据的处理上能力非常强，但是如果时序数据是图像，则在LSTM的基础上加上卷积操作，对于图像的特征提取会更加有效。</div>
              </div>
            </div>
            <div class="col-sm-2 col-lg-12">
              <div class="iq-card" >
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">SEIR</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade3"
                  >
                    查看详情
                  </a>
                </div>
                </div>
                <div class="iq-card-body">SEIR(Susceptible-Exposed-Infected-Removed)，类似于SIR，但是增加了对潜伏期的定义，因此更适用于具有一定潜伏期的传染病。状态之间的转化如下所示：</div>
              </div>
            </div>
          </div>

          <div class="row box animated flipInX" id="f1"  v-if="show1">
            <div class="col-sm-2 col-lg-12">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">Convlution</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade11"
                  >
                    <i class="ri-reply-fill"></i>
                    返回
                  </a>
                </div>
                </div>
                <div class="iq-card-body">
                  <img
                    class="col-lg-12"
                    src="../../images/principle/conv.png"
                    alt="convlution"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="row box animated flipInX" id="f2" v-if="show2">
            <div class="col-sm-2 col-lg-12">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">ConvLSTM</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade21"
                  >
                    <i class="ri-reply-fill"></i>
                    返回
                  </a>
                </div>
                </div>
                <div class="iq-card-body">
                  <img
                    class="col-lg-12"
                    src="../../images/principle/convLSTM.png"
                    alt="ConvLSTM"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="row box animated flipInX" id="f3" v-if="show3">
            <div class="col-sm-2 col-lg-12">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">SEIR</h4>
                  </div>
                  <div class="chat-header-icons d-flex">
                  <a
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 80px; font-size: 14px; margin-top: 18px"
                    @click="fade31"
                  >
                    <i class="ri-reply-fill"></i>
                    返回
                  </a>
                </div>
                </div>
                <div class="iq-card-body">
                  <img
                    class="col-lg-12"
                    src="../../images/principle/seir.png"
                    alt="SEIR"
                  />
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>
    <!-- Wrapper END -->
    <!-- Footer -->
    <footer class="bg-white iq-footer" style="z-index: 1">
      <div class="container-fluid">
        <div class="row">
          <div class="col-lg-6">
            <ul class="list-inline mb-0">
              <li class="list-inline-item">
                <a href="privacy-policy.html">Privacy Policy</a>
              </li>
              <li class="list-inline-item">
                <a href="terms-of-service.html">Terms of Use</a>
              </li>
            </ul>
          </div>
          <div class="col-lg-6 text-right">
            Copyright 2020 <a href="#">Vito</a> All Rights Reserved.
          </div>
        </div>
      </div>
    </footer>

    <!-- </div> -->
  </div>
</template>
<script src="https://www.jq22.com/jquery/jquery-1.10.2.js"></script>
<script>
import animate from "../../css/animate.css";
export default {
  data() {
    return {
      value:new Date(),
      // 头像
      fits: ["fill"],
      AdminUrl: "",
      MyContent: [],
      AdminId: "",
      AdminAuthority: 1,
      authorityShow: false,
      show: true,
      show1: false,
      show2: false,
      show3: false,
    };
  },
  created: function () {
    this.getMyIdentity();
  },
  methods: {
    //获取管理员身份
    getMyIdentity: function () {
      var self = this;
      axios
        .post("/apis/backend/getIdentity/")
        .then((response) => {
          this.AdminId = response.data.userId;
          this.AdminAuthority = response.data.authority;
          if (
            response.data.authority == 2 ||
            response.data.authority == 3
          ) {
            this.authorityShow = true;
            this.getMyContent();
          } else {
            this.$message("您没有权限进入管理员界面！");
            this.$router.push({
              path: "/UserProfile",
            });
          }
        })
        .catch(function (error) {
          alert(JSON.stringify(error));
          alert("获取用户身份失败");
        });
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/" + this.AdminId + "/")
        .then((response) => {
          (self.MyContent = response.data),
            (this.AdminUrl = self.MyContent.avatar_url);
        })
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    adminOrSuperAdmin: function () {
      if (this.AdminAuthority == 3) {
        this.$router.push({
          path: "/SuperUserManage",
        });
      } else if (this.AdminAuthority == 2) {
        this.$router.push({
          path: "/AdminUserManage",
        });
      }
    },
    fade1: function () {
      $("#f").addClass("animated flipOutX");
      this.show=false;
      this.show1 = true;
    },
    fade11: function () {
      $("#f1").addClass("animated flipOutX");
      this.show=true;
      this.show1 = false;
    },
    fade2: function () {
      $("#f").addClass("animated flipOutX");
      this.show=false;
      this.show2 = true;
    },
    fade21: function () {
      $("#f2").addClass("animated flipOutX");
      this.show=true;
      this.show2 = false;
    },
    fade3: function () {
      $("#f").addClass("animated flipOutX");
      this.show=false;
      this.show3 = true;
    },
    fade31: function () {
      $("#f3").addClass("animated flipOutX");
      this.show=true;
      this.show3 = false;
    },
  },
};
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css";
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
/* @import "../../images/favicon.ico"; */
@import "../../css/style.css";
.avatar-md img {
  width: 38px;
}
.rounded-circle {
  border-radius: 50% !important;
}
/* 日历组件 */
.el-calendar-table .el-calendar-day {
  height: 40px;
}
.el-calendar-table .el-calendar-day:hover {
  background: #d8c5f8;
}
.el-calendar-table td.is-selected {
  background-color: #dbc7fc;
  color: #fff;
}
.el-calendar-table td.is-today {
  color: #9150f8;
  /* color:rgb(125, 201, 224);
  color:rgb(132, 223, 215);
  color:rgb(150, 188, 245) */
}
#calendar {
  border: 0px;
  margin-top: 10px;
  background: transparent;
}
#calendar :hover {
  background: transparent;
}
.goodlist {
  width: 200px;
  height: 200px;
  background: red;
  animation-duration: 2s;
}
/* 从隐藏到显示 */
.fade-enter {
  opacity: 0;
}
.fade-enter-active,
.active {
  transition: opacity 3s;
}
/* 从显示到隐藏 */
.fade-leave-to {
  opacity: 0;
}
.fade-leave-active,
.leave {
  transition: opacity 3s;
}
</style>
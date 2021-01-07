<template>
  <div v-if="ifShow" style="background-color: rgb(235, 234, 250)">
    <div class="wrapper">
      <!-- Sidebar  -->
      <div class="iq-sidebar" style="z-index: 1">
        <div class="iq-sidebar-logo d-flex justify-content-between">
          <span style="font-size: 18px">高传染性疾病预测系统</span>
        </div>
        <div id="sidebar-scrollbar">
          <nav class="iq-sidebar-menu">
            <ul class="iq-menu" style="margin-top: 20px">
              <li class="active">
                <a class="iq-waves-effect"
                  ><i class="ri-profile-line"></i><span>个人资料</span></a
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: 'UserProfileEdit',
                    query: { uI: this.userId },
                  }"
                  ><i class="ri-file-edit-line"></i
                  ><span>修改资料</span></router-link
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/UserCase',
                    query: { uI: this.userId },
                  }"
                  ><i class="ri-file-list-line"></i
                  ><span>我的案例</span></router-link
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
              <li v-if="ifAdmin">
                <div class="chat-header-icons d-flex">
                  <router-link
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 100px; font-size: 14px; margin-top: 18px; margin-right:10px;"
                    :to="{
                      path: '/AdminIndex',
                    }"
                  >
                    <i class="ri-reply-fill"></i>
                    进入后台
                  </router-link>
                </div>
              </li>
              <li>
                <div class="chat-header-icons d-flex">
                  <router-link
                    class="chat-icon-phone iq-bg-primary"
                    style="width: 100px; font-size: 14px; margin-top: 18px"
                    :to="{
                      path: '/UserIndex',
                    }"
                  >
                    <i class="ri-reply-fill"></i>
                    返回前台
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
                  <img :src="Url" class="img-fluid rounded mr-3" alt="user" />
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
      <div id="content-page" class="content-page" style="z-index: 1">
        <div class="container-fluid">
          <div class="row">
            <div class="col-lg-6" style="left: 25%">
              <div class="iq-edit-list-data">
                <div class="tab-content">
                  <div
                    class="tab-pane fade active show"
                    id="personal-information"
                    role="tabpanel"
                  >
                    <div class="iq-card">
                      <div class="iq-card-body">
                        <div class="imf">
                          <ul
                            id="todo-task1"
                            class="sub-task show mt-2 p-0"
                            style="list-style-type: none"
                          >
                            <li>
                              <!-- <div class="demo-fit"> -->
                              <div
                                class="block"
                                v-for="fit in fits"
                                :key="fit"
                                style="text-align: center"
                              >
                                <el-avatar
                                  shape="circle"
                                  :size="70"
                                  :src="Url"
                                ></el-avatar>
                              </div>
                              <!-- </div> -->
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-success"
                                ></i>
                                <span style="font-size: 18px">
                                  昵称： {{ MyContent.userName }}
                                </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-warning"
                                ></i>
                                <span style="font-size: 18px">
                                  性别： {{ MyContent.sex }}
                                </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-danger"
                                ></i>
                                <span style="font-size: 18px">
                                  出生日期： {{ MyContent.birth }}
                                </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-primary"
                                ></i
                                ><span style="font-size: 18px">
                                  手机号： {{ MyContent.phoneNumber }}
                                </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-info"
                                ></i>
                                <span style="font-size: 18px">
                                  邮箱： {{ MyContent.email }}
                                </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px; margin-left: 30%">
                              <h5>
                                <i
                                  class="ri-checkbox-blank-circle-fill text-dark"
                                ></i>
                                <span style="font-size: 18px">
                                  住址： {{ MyContent.address }}
                                </span>
                              </h5>
                            </li>
                            <button
                              style="margin-top: 40px"
                              type="button"
                              class="btn btn-primary btn-block"
                              @click="handleLogout()"
                            >
                              注销
                            </button>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ifShow:false,
      value: new Date(),
      // 头像
      fits: ["fill"],
      Url: "",
      MyContent: [],
      userId: "",
      userAuthority:1,
      ifAdmin:false
    };
  },
  created: function () {
    this.GetUserIdentity();
    // this.Admin()
    // alert(this.userAuthority)
    // alert(this.ifAdmin)
    // this.getMyContent();
  },
  methods: {
    Show(){
      if(this.ifLogin=="返回数据成功"){
        this.ifShow=true
        this.getMyContent()
      }
      else{
        this.$message("你尚未登录")
        this.$router.push({
              path:'/Login'
          });
      }
    },
    //判断是否管理员
    Admin(){
      if(this.userAuthority==2||this.userAuthority==3){
        this.ifAdmin=true
      }
    },
    //获取用户身份
    GetUserIdentity() {
      var self = this;
      // alert("获取用户身份")
      axios
        .post("/apis/backend/getIdentity/")
        .then(
          (response) => (
            self.userId = response.data.userId,
            self.userAuthority=response.data.authority,
            self.ifLogin=response.data.message,
            // alert(JSON.stringify(response.data)),
            this.Show(),
            this.Admin()
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/" + this.userId + "/")
        .then(
          (response) => (
            (self.MyContent = response.data),
            // alert(JSON.stringify(response.data)),
            (this.Url = self.MyContent.avatarUrl)
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("getMyContent数据请求失败wdnmd");
        });
    },
    handleLogout: function () {
      this.$confirm("确认退出吗？", "系统提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.logout();
          this.$message({
            type: "success",
            message: "退出成功！",
          });
          this.$router.push({
            path: "/Login",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消退出！",
          });
        });
    },
    logout: function () {
      var self = this;
      axios.get("/apis/backend/logout/").catch(function (error) {
        alert("数据请求失败wdnmd");
      });
    },
  },
};
</script>

<style scoped>
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
</style>
<style>
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
}
#calendar {
  border: 0px;
  margin-top: 20px;
  background: transparent;
}
#calendar :hover {
  background: transparent;
}
</style>
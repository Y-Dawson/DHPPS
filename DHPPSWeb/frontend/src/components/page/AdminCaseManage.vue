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
              <li class="active">
                <a class="iq-waves-effect"
                  ><i class="ri-home-4-line"></i><span>案例管理</span></a
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminModelView',
                  }"
                  ><i class="ri-home-4-line"></i
                  ><span>查看模型</span></router-link
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
      <div
        id="content-page"
        class="content-page"
        style="z-index: 1"
        v-if="!show"
      >
        <div class="container-fluid">
          <div class="row">
            <div class="col-sm-12">
              <div class="iq-card">
                <div class="iq-card-body">
                  <div class="">
                    <table
                      id="user-list-table"
                      class="table mt-4"
                      role="grid"
                      aria-describedby="user-list-page-info"
                    >
                      <thead>
                        <tr style="text-align: center">
                          <th style="width: 10%">ID</th>
                          <th style="width: 15%">昵称</th>
                          <th style="width: 15%">手机号</th>
                          <th style="width: 10%">案例数量</th>
                          <th style="width: 20%">备注</th>
                          <th style="width: 20%">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in content"
                          :key="item.userId"
                          style="text-align: center"
                        >
                          <td>{{ item.userId }}</td>
                          <td>{{ item.userName }}</td>
                          <td>{{ item.phoneNumber }}</td>
                          <td>
                            <span class="badge iq-bg-primary">{{
                              item.caseNumber
                            }}</span>
                          </td>
                          <td>{{ item.remark }}</td>
                          <td>
                            <div
                              class="flex align-items-center list-user-action"
                            >
                              <a
                                class="iq-bg-primary"
                                style="width: 80px"
                                data-toggle="tooltip"
                                data-placement="top"
                                title=""
                                data-original-title="Edit"
                                @click="SwitchPage(item.userId)"
                              >
                                查看案例
                              </a>
                            </div>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <hr />
                  <div class="row justify-content-between mt-3">
                    <div id="user-list-page-info" class="col-md-6">
                      <span>Showing 1 to 5 of 5 entries</span>
                    </div>
                    <div class="col-md-6">
                      <nav aria-label="Page navigation example">
                        <ul class="pagination justify-content-end mb-0">
                          <li class="page-item">
                            <a
                              class="page-link"
                              tabindex="-1"
                              aria-disabled="true"
                              @click="prevPage()"
                              >Previous</a
                            >
                          </li>
                          <li class="page-item">
                            <a class="page-link"
                              >第{{ currentPage }}页/共{{ totalPage }}页</a
                            >
                          </li>
                          <li class="page-item">
                            <a class="page-link" @click="nextPage()">Next</a>
                          </li>
                        </ul>
                      </nav>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        id="content-page"
        class="content-page box animated pulse"
        style="z-index: 1"
        v-if="show"
      >
        <div class="chat-header-icons d-flex" style="padding: 5px 15px">
          <a
            href="javascript:void();"
            class="chat-icon-phone iq-bg-primary"
            style="width: 100px"
            @click="ClosePage()"
          >
            <i class="ri-reply-fill"></i>
            返回
          </a>
        </div>
        <div style="padding: 15px;z-index: 2">
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <div class="layui-tab-content">
              <div class="box" style="text-align: center">
                <div
                  class="box-card-group"
                  style="
                    margin-left: 10%;
                    margin-top: 20px;
                    margin-bottom:10px;
                    width: auto;
                    height: 480px;
                    text-align: left;
                  ">
                  <el-col
                    :span="7"
                    v-for="(item, index) in currentPageData.data"
                    :key="index"
                  >
                    <el-card class="box-card">
                      <div slot="header" class="clearfix">
                        <i v-if="item.caseMode === 1"
                          class="el-icon el-icon-location-outline"
                          style="
                            margin-right: 10px;
                            font-size: 38px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <i v-else-if="item.caseMode === 2"
                          class="el-icon el-icon-map-location"
                          style="
                            margin-right: 10px;
                            font-size: 38px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <span id="returnContent">{{ item.caseName }}</span>
                        <div
                          style="
                            font-size: 18px;
                            line-height: 20px;
                            float: right;
                            text-align: right;
                          "
                        >
                        </div>
                      </div>
                      <dl class="box-text">
                        <span>初始城市数量：</span>
                        <span id="returnContent">{{ item.cityNumber }}</span>
                        <br />
                        <span>初始道路数量：</span>
                        <span id="returnContent">{{ item.roadNumber }}</span>
                        <br />
                        <span>初始总人口：</span>
                        <span id="returnContent">{{ item.initTotal }}</span>
                        <br />
                        <span>初始感染人口：</span>
                        <span id="returnContent">{{
                          item.initTotalInfected
                        }}</span>
                      </dl>
                    </el-card>
                  </el-col>
                </div>

                <div>
                  <nav aria-label="Page navigation example">
                    <ul class="pagination mb-0" style="justify-content: center">
                      <li class="page-item">
                        <a
                          class="page-link"
                          tabindex="-1"
                          aria-disabled="true"
                          @click="GetPrevCasePage()"
                          >Previous</a
                        >
                      </li>
                      <li class="page-item">
                        <a class="page-link"
                          >第{{ currentCasePage }}页/共{{ totalCasePage }}页</a
                        >
                      </li>
                      <li class="page-item">
                        <a class="page-link" @click="GetNextCasePage()">Next</a>
                      </li>
                    </ul>
                  </nav>
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

<script>
export default {
  data() {
    return {
      value:new Date(),
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      AdminUrl: "",
      AdminAuthority: 1,
      authorityShow: false,
      //用户信息列表
      content: [],
      //用户案例列表
      cases: [],
      casenum: 8,
      test: 0,
      MyContent: [],
      AdminId: "25",
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 4, // 每页显示数量
      paginate: 10,
      //分页
      totalCasePage: 1, // 统共页数，默认为1
      currentCasePage: 1, //当前页数 ，默认为1
      pageCaseSize: 6, // 每页显示数量
      currentPageData: [], //当前页显示内容
      //用户编辑的id和昵称
      UserId: "",
      UserName: "",
      show: false,
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
            this.getMyContent(), this.getUserContent();
          } else {
            this.$message("您没有权限进入管理员界面！");
            this.$router.push({
              path: "/UserProfile",
            });
          }
        })
        .catch(function (error) {
          alert("获取用户身份失败");
        });
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/" + this.AdminId + "/")
        .then(
          (response) => (
            (self.MyContent = response.data),
            (this.AdminUrl = self.MyContent.avatar_url)
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    getUserContent: function () {
      axios
        .get("/apis/backend/userManage/", {
          params: {
            pageSize: 10,
            page: this.currentPage,
          },
        })
        .then(
          (response) => (
            (this.content = response.data.data),
            (this.paginate = response.data.pagination),
            (this.pageSize = response.data.pageSize),
            (this.totalPage = Math.ceil(this.paginate / this.pageSize)),
            this.testPage()
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    SwitchPage: function (UI) {
      (this.UserId = UI),
      this.currentCasePage=1,
      this.GetCaseContent();
      this.SetPages();
      (this.show = true);
      
    },
    ClosePage: function () {
      this.show = false;
      this.getUserContent();
    },
    //获取案例内容
    GetCaseContent: function () {
      var self = this;
      alert(this.UserId),
      axios
        .get("/apis/backend/case/", {
          params: {
            userId: this.UserId,
            pageSize: 6,
            page: self.currentCasePage,
          },
        })
        .then(
          (response) => 
          (
            (this.currentPageData = response.data),
            (this.totalCasePage = Math.ceil(response.data.pagination / response.data.pageSize)),
            this.SetPages()
          )
          // (
          //   alert(JSON.stringify(response.data)),
          //   (self.currentPageData = response.data),
          //   (self.totalCasePage = Math.ceil(
          //     self.currentPageData.pagination / self.pageCaseSize
          //   )),
          //   (self.SetPages())
          // )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败");
        });
    },

    //上一页
    prevPage() {
      if (this.currentPage == 1) return;
      this.currentPage--;
      this.getUserContent();
    },
    // 下一页
    nextPage() {
      if (this.currentPage == this.totalPage) return;
      this.currentPage++;
      this.getUserContent();
    },
    testPage: function () {
      if (this.totalPage == 0) this.totalPage = 1;
    },
    //上一页
    GetPrevCasePage() {
      if (this.currentCasePage == 1) return;
      this.currentCasePage--;
      this.GetCaseContent();
    },
    // 下一页
    GetNextCasePage() {
      if (this.currentCasePage == this.totalCasePage) return;
      this.currentCasePage++;
      this.GetCaseContent();
    },
    SetPages() {
      if (this.totalCasePage < 1) this.totalCasePage = 1;
    },
    handleDel(UI) {
      this.$confirm("确认删除该用户吗？", "系统提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.deleteContent(UI);
          this.$message({
            type: "success",
            message: "删除成功！",
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消删除！",
          });
        });
    },
    deleteContent: function (UI) {
      var self = this;
      // var date = $("#input1").val();
      axios
        .delete("/apis/backend/accountInfo/" + UI + "/", {})
        .then(
          (response) => (
            (self.content = response), self.getUserContent()
            // alert(JSON.stringify(response))
          )
        )
        .catch(function (error) {
          alert("数据发送失败");
          console.log(error.response);
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
  },
};
</script>

<style scoped>
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
.avatar-md img {
  width: 38px;
}
.rounded-circle {
  border-radius: 50% !important;
}
.mask {
  background-color: #000;
  opacity: 0.3;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}
.pop {
  background-color: #fff;

  position: fixed;
  top: 100px;
  left: 300px;
  width: calc(100% - 600px);
  height: calc(100% - 200px);
  z-index: 2;
}
.btn {
  background-color: #fff;
  border-radius: 4px;
  padding: 4px 12px;
}
/* 案例块文字内容 */
.box-text {
  margin-left: 5px;
  line-height: 20px;
  font-size: 14px;
  color: rgb(71, 71, 71);
}
/* 案例块样式 */
.box-card {
  border-radius: 14px;
  width: 250px;
  /* float: left; */
  margin-right: 180px;
  margin-bottom: 20px;
}
.reset {
  background: #fff;
  border: 1px #55587e solid;
}
.el-checkbox :hover {
  background: #8b9bbd;
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
}
#calendar {
  border: 0px;
  margin-top: 10px;
  background: transparent;
}
#calendar :hover {
  background: transparent;
}
</style>
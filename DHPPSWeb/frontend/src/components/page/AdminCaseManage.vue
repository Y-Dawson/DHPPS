<template>
  <div style="background-color: rgb(235, 234, 250)">
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
                    query: { uI: this.AdminUserId },
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
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminUserManage',
                    query: { uI: this.AdminUserId },
                  }"
                  ><i class="ri-user-line"></i
                  ><span>信息管理</span></router-link
                >
              </li>
              <li class="active">
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/SuperCaseManage',
                    query: { uI: this.AdminUserId },
                  }"
                  ><i class="ri-home-4-line"></i><span>案例管理</span></router-link
                >
              </li>
              <li>
                <a href="#" class="iq-waves-effect"
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
          <!-- <div class="iq-sidebar-logo">
               <div class="top-logo">
                  <a href="index.html" class="logo">
                  <img src="images/logo.gif" class="img-fluid" alt="">
                  <span>vito</span>
                  </a>
               </div>
            </div> -->
          <nav class="navbar navbar-expand-lg navbar-light p-0">
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav ml-auto navbar-list">
                <li class="nav-item">
                  <a class="search-toggle iq-waves-effect" href="#"
                    ><i class="ri-calendar-line"></i
                  ></a>
                  <div class="iq-sub-dropdown">
                    <div class="calender-small"></div>
                  </div>
                </li>
              </ul>
            </div>
            <ul class="navbar-list">
              <li>
                <a
                  href="#"
                  class="search-toggle iq-waves-effect d-flex align-items-center"
                >
                  <img
                    :fit="fit"
                    :src="AdminUrl"
                    class="img-fluid rounded mr-3"
                    alt="user"
                  />
                  <div class="caption">
                    <h6 class="mb-0 line-height">{{ MyContent.username }}</h6>
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
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <div class="chat-header-icons d-flex">
                      <a
                        href="javascript:void();"
                        class="chat-icon-phone iq-bg-primary"
                        style="width: 120px"
                      >
                        <i class="ri-file-mark-fill"></i>
                        案例管理
                      </a>
                    </div>
                  </div>
                </div>
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
                          :key="item.userid"
                          style="text-align: center"
                        >
                          <td>{{ item.userid }}</td>
                          <td>{{ item.username }}</td>
                          <td>{{ item.phonenumber }}</td>
                          <td>
                            <span class="badge iq-bg-primary">{{
                              item.casenumber
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
                                @click="SwitchPage(item.userid)"
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
        class="content-page"
        style="z-index: 1"
        v-if="show"
      >
        <div class="chat-header-icons d-flex">
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
        <div style="padding: 15px；z-index: 2">
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <div class="layui-tab-content">
              <div class="box" style="text-align: center">
                <div
                  class="box-card-group"
                  style="
                    margin-left: 60px;
                    margin-top: 20px;
                    width: auto;
                    height: 450px;
                    text-align: left;
                  "
                >
                  <el-col
                    :span="7"
                    v-for="(item, index) in currentPageData.data"
                    :key="index"
                  >
                    <el-card class="box-card">
                      <div slot="header" class="clearfix">
                        <i
                          class="layui-icon layui-icon-template-1"
                          style="
                            margin-right: 10px;
                            font-size: 40px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <span id="returnContent">{{ item.casename }}</span>
                        <div
                          style="
                            font-size: 8px;
                            line-height: 20px;
                            float: right;
                            text-align: right;
                          "
                        >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: #55587e"
                            @click="edit(item.caseid)"
                            >进入编辑</el-button
                          >
                          <br />
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: rgb(221, 0, 0)"
                            @click="open(item.caseid)"
                            >删除</el-button
                          >
                        </div>
                      </div>
                      <dl class="box-text">
                        <!-- <span>{{casenum}}</span> -->
                        <span>初始城市数量：</span>
                        <span id="returnContent">{{ item.citynumber }}</span>
                        <br />
                        <span>初始道路数量：</span>
                        <span id="returnContent">{{ item.roadnumber }}</span>
                        <br />
                        <span>初始总人口：</span>
                        <span id="returnContent">{{ item.inittotal }}</span>
                        <br />
                        <span>初始感染人口：</span>
                        <span id="returnContent">{{
                          item.inittotalinfected
                        }}</span>
                        <!-- <span id="returnContent" style="color:black;">{{ ccontent.themename }}</span> -->
                        <!-- <span id="returnContent">{{ content }}</span> -->
                        <!-- <span id="returnContent">{{ content.themeno }}</span> -->
                      </dl>
                    </el-card>
                  </el-col>
                </div>
                <div class="paginate">
                  <button class="primaryb" @click="prevPage()">上一页</button>
                  <span>第{{ currentPage }}页/共{{ totalPage }}页</span>
                  <button class="primaryb" @click="nextPage()">下一页</button>
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
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      AdminUrl: "",
      //用户信息列表
      content: [],
      //用户案例列表
      cases: [],
      currentPageData: [], //当前页显示案例内容
      casenum: 8,
      test: 0,
      MyContent: [],
      AdminId: "25",
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 4, // 每页显示数量
      paginate: 10,
      //用户编辑的id和昵称
      UserId: "",
      UserName: "",
      show: false,
    };
  },
  created: function () {
    this.getMyContent(), this.getUserContent();
  },
  methods: {
    getMyContent: function () {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/profile/25/")
        .then(
          (response) => (
            (self.MyContent = response.data),
            (this.AdminUrl = self.MyContent.avatar)
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    getUserContent: function () {
      axios
        .get("http://127.0.0.1:8000/backend/generalUserManage/", {
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
    PostUserMessage: function (UI) {
      var self = this;
      alert($("#RemarkMessage").val()),
        alert(UI),
        alert($("#selected").val()),
        axios
          .put("http://127.0.0.1:8000/backend/accountInfo/" + UI + "/", {
            remark: $("#RemarkMessage").val(),
            authority: $("#selected").val(),
          })
          .then(
            (response) => (
              alert(26),
              this.$message("修改权限成功"),
              alert(JSON.stringify(response))
            )
          )
          .catch(function (error) {
            alert("数据发送失败");
          });
    },
    SwitchPage: function (UI) {
      (this.UserId = UI), (this.show = true);
      getCaseContent(UI);
    },
    ClosePage: function () {
      this.show = false;
    },
    //获取案例内容
    getCaseContent: function () {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/case/", {
          params: {
            userid: this.$route.query.userId,
            page_size: 6,
            page: self.currentPage,
          },
        })
        .then(
          (response) => (
            (self.currentPageData = response.data),
            // alert(JSON.stringify(this.currentPageData))
            (self.totalPage = Math.ceil(
              self.currentPageData.pagination / self.pageSize
            ))
            //
          )
        )
        .catch(function (error) {
          // 请求失败处理
          // alert('数据请求失败wdnmd')
        });
    },
    edit: function (id) {
      var self = this;
      let data = new FormData();
      data.append("caseid", id);
      axios
        .post("http://127.0.0.1:8000/backend/getCaseInfo/", data)
        .then((response) => {
          self.cases = response.data.cases;
          console.log(JSON.stringify(self.cases));

          console.log(self.cases.Initcitydata);
          var city_inf = [];
          for (var j in self.cases.Initcitydata) {
            var s =
              "cityname:" +
              self.cases.Initcitydata[j].cityname +
              ",initpop:" +
              self.cases.Initcitydata[j].initpop +
              ",initinfect:" +
              self.cases.Initcitydata[j].initinfect;
            console.log("s:", s);
            city_inf.push(s);
          }

          var road_inf = [];
          for (var j in self.cases.Initroaddata) {
            var s =
              "departure:" +
              self.cases.Initroaddata[j].departure +
              ",destination:" +
              self.cases.Initroaddata[j].destination +
              ",volume:" +
              self.cases.Initroaddata[j].volume;
            console.log("s:", s);
            road_inf.push(s);
          }

          var city_pos = [];
          for (var j in self.cases.Cityposition) {
            var s =
              "cityname:" +
              self.cases.Cityposition[j].cityname +
              ",x:" +
              self.cases.Cityposition[j].x +
              ",y:" +
              self.cases.Cityposition[j].y;
            console.log("s:", s);
            city_pos.push(s);
          }

          this.$router.push({
            path: "/setting",
            query: {
              params: JSON.stringify({
                userId: this.userId,
                casename: this.cases.casename,
                citynum: this.cases.citynum,
                roadnum: this.cases.roadnum,
                Initcitydata: city_inf,
                Initroaddata: road_inf,
                Cityposition: city_pos,
              }),
            },
          });
        })
        .catch(function (error) {
          // 请求失败处理
          // alert(JSON.stringify(response));
          alert(JSON.stringify(error.response));
          alert("数据请求失败wdnmd");
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
        .delete("http://127.0.0.1:8000/backend/accountInfo/" + UI + "/", {})
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
  line-height: 18px;
  font-size: 12px;
  color: rgb(71, 71, 71);
}
/* 案例块样式 */
.box-card {
  width: 240px;
  float: left;
  margin-right: 50px;
  margin-bottom: 20px;
}
.reset {
  background: #fff;
  border: 1px #55587e solid;
}
.el-checkbox :hover {
  background: #8b9bbd;
}
</style>
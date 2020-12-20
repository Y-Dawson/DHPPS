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
              <li class="active">
                <a class="iq-waves-effect"
                  ><i class="ri-user-line"></i><span>信息管理</span></a
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminCaseManage',
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
      <div id="content-page" class="content-page" style="z-index: 1">
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
                        style="width:120px"
                      >
                        <i class="ri-user-3-line"></i>
                        用户管理
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
                          <th style="width: 8%">ID</th>
                          <th style="width: 8%">头像</th>
                          <th style="width: 10%">昵称</th>
                          <th style="width: 10%">手机号</th>
                          <th style="width: 10%">邮箱</th>
                          <th style="width: 10%">案例数量</th>
                          <th style="width: 20%">备注</th>
                          <th style="width: 10%">创建时间</th>
                          <th style="width: 14%">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="item in content"
                          :key="item.userid"
                          style="text-align: center"
                        >
                          <td>{{ item.userid }}</td>
                          <td class="text-center">
                            <div class="avatar avatar-md">
                              <img
                                :fit="fit"
                                :src="item.avatar"
                                class="img-fluid rounded mr-3"
                              />
                            </div>
                          </td>
                          <!-- <td>
                          <el-avatar
                              shape="circle"
                              :size="30"
                              :fit="fit"
                              :src="item.avatar"
                           ></el-avatar>
                           </td> -->
                          <td>{{ item.username }}</td>
                          <td>{{ item.phonenumber }}</td>
                          <td>{{ item.email }}</td>
                          <td>
                            <span class="badge iq-bg-primary">{{
                              item.casenumber
                            }}</span>
                          </td>
                          <td>{{ item.remark }}</td>
                          <td>{{ item.createdate }}</td>
                          <td>
                            <div
                              class="flex align-items-center list-user-action"
                            >
                              <a
                                class="iq-bg-primary"
                                data-toggle="tooltip"
                                data-placement="top"
                                title=""
                                data-original-title="Edit"
                                @click="
                                  UserEdit(item.userid, item.username, true)
                                "
                              >
                                <i class="ri-pencil-line"></i>
                              </a>
                              <a
                                class="iq-bg-primary"
                                data-toggle="tooltip"
                                data-placement="top"
                                title=""
                                data-original-title="Delete"
                                @click="handleDel(item.userid)"
                                ><i class="ri-delete-bin-line"></i
                              ></a>
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
                    <!-- <div class="paginate">
                        <button class="primaryb" @click="prevPage()">
                        上一页
                        </button>
                        <span>第{{currentPage}}页/共{{totalPage}}页</span>
                        <button class="primaryb" @click="nextPage()">
                        下一页
                        </button>
                    </div> -->
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
    <div class="mask" v-if="showModal" @click="showModal = false"></div>
    <!-- <div class="pop" v-if="true"> -->
    <div
      id="item1"
      v-if="showModal"
      class="iq-card"
      style="
        background-color: #fff;
        position: fixed;
        top: 50px;
        left: 400px;
        width: calc(100% - 800px);
        height: calc(100%-200px);
        z-index: 999;
      "
    >
      <div class="container-fluid">
        <div class="iq-card-header d-flex justify-content-between">
          <div class="iq-header-title">
            <h4 class="card-title">编辑</h4>
          </div>
        </div>
        <div class="iq-card-body">
          <form>
            <div class="form-group">
              <label for="exampleInputDisabled1">用户昵称</label>
              <input
                type="text"
                class="form-control"
                id="exampleInputDisabled1"
                disabled=""
                :value="UserName"
              />
            </div>
            <div class="form-group">
              <label for="exampleFormControlTextarea1">备注</label>
              <textarea
                class="form-control"
                id="RemarkMessage"
                rows="4"
              ></textarea>
            </div>
            <div class="form-group">
              <label for="exampleFormControlTextarea1">权限</label>
              <select id="selected" v-model="selected" name="authority">
                <option value="普通用户">普通用户</option>
                <option value="管理员">管理员</option>
              </select>
            </div>
            <div style="text-align: right">
              <button
                type="submit"
                class="btn btn-primary"
                @click="PostUserMessage(UserId)"
              >
                提交
              </button>
              <button
                type="submit"
                class="btn iq-bg-danger"
                @click="CloseUserEdit(false)"
              >
                取消
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- </div> -->
  </div>
</template>

<script>
// import custom from "../../js/custom.js";
// import smooth from "../../js/smooth-scrollbar.js";
// import magnific from "../../js/jquery.magnific-popup.min.js";
// import select2 from "../../js/select2.min.js";
// import slick from "../../js/slick.min.js";
// import wow from "../../js/wow.min.js";
// import counterup from "../../js/jquery.counterup.min.js";
// import popper from "../../js/popper.min.js";
// import popup from "../../js/jquery.popup.js";
export default {
  data() {
    return {
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      AdminUrl: "",
      content: [],
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
      showModal: false,
      radioVal: "普通用户",
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
    UserEdit: function (UI, UN, show) {
      (this.UserId = UI), (this.UserName = UN), (this.showModal = show);
    },
    CloseUserEdit: function (show) {
      this.showModal = show;
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
</style>
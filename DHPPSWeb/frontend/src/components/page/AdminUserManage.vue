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
                  }"
                  ><i class="ri-home-4-line"></i
                  ><span>案例管理</span></router-link
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
      <div id="content-page" class="content-page" style="z-index: 1">
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
                          <th style="width: 8%">ID</th>
                          <th style="width: 5%">头像</th>
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
                          :key="item.userId"
                          style="text-align: center"
                        >
                          <td>{{ item.userId }}</td>
                          <td>
                            <div class="avatar avatar-md">
                              <img
                                :src="item.avatarUrl"
                                class="img-fluid rounded mr-3"
                                alt="user"
                              />
                            </div>
                          </td>
                          <!-- <td>
                          <el-avatar
                              shape="circle"
                              :size="30"
                              :src="item.avatar"
                           ></el-avatar>
                           </td> -->
                          <td>{{ item.userName }}</td>
                          <td>{{ item.phoneNumber }}</td>
                          <td>{{ item.email }}</td>
                          <td>
                            <span class="badge iq-bg-primary">{{
                              item.caseNumber
                            }}</span>
                          </td>
                          <td>{{ item.remark }}</td>
                          <td>{{ item.createDate }}</td>
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
                                  UserEdit(
                                    item.userId,
                                    item.userName,
                                    item.remark,
                                    item.authority,
                                    true
                                  )
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
                                @click="handleDel(item.userId)"
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
                    <div class="col-md-12">
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
                placeholder="请输入备注......（最多输入100个字）"
                @input="descInput"
                v-model="desc"
                maxlength="100"
              ></textarea>
              <!-- <span>{{ txtVal }}/500</span> -->
            </div>
            <div class="form-group">
              <label for="exampleFormControlTextarea1">权限</label>
              <select id="selected" v-model="selected" name="authority">
                <option value="普通用户" selected="selected">普通用户</option>
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

<script type="text/javascript">
document.οnkeydοwn = function () {
  var myEvent = event ? event : window.event ? window.event : null;
  var keycode = myEvent.keyCode;
  if (myEvent.keyCode == 13) {
    console.log("接收到回车");
    myEvent.keyCode = 9;
    myEvent.returnValue = false;
  }
};
</script>
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
      value: new Date(),
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      AdminUrl: "",
      content: [],
      MyContent: [],
      AdminId: "",
      authorityShow: false,
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 4, // 每页显示数量
      paginate: 10,
      //用户编辑的id和昵称
      UserId: "",
      UserName: "",
      UserRemark: "",
      UserAuthority: 1,
      showModal: false,
      radioVal: "普通用户",

      txtVal: 0,
      desc: "",
    };
  },
  created: function () {
    this.getMyIdentity();
  },
  methods: {
    //获取管理员身份
    getMyIdentity() {
      var self = this;
      axios
        .post("/apis/backend/getIdentity/")
        .then((response) => {
          this.AdminId = response.data.userId;
          if(response.data.message=="未登录") {
            this.$message("您尚未登录");
            this.$router.push({
              path: "/Login",
            });
          }
          else if (response.data.authority == 2 || response.data.authority == 3) {
            this.authorityShow = true;
            this.getMyContent();
            this.getUserContent();
          } else {
            this.$message("您没有权限进入管理员界面！");
            this.$router.push({
              path: "/UserProfile",
            });
          }
        })
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
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
            (this.AdminUrl = self.MyContent.avatarUrl)
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    getUserContent: function () {
      axios
        .get("/apis/backend/generalUserManage/", {
          params: {
            pageSize: 10,
            page: this.currentPage,
          },
        })
        .then(
          (response) => (
            // alert(JSON.stringify(response.data.data)),
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
      if ($("#RemarkMessage").val() !== "") {
        self.UserRemark = $("#RemarkMessage").val();
      }
      if ($("#selected").val() == "管理员") {
        self.UserAuthority = 2;
      } else if ($("#selected").val() == "普通用户") {
        self.UserAuthority = 1;
      } else if ($("#RemarkMessage").val() == "") {
        this.$message("请选择需要修改的内容");
        return;
      }
      axios
        .put("/apis/backend/accountInfo/" + UI + "/", {
          remark: self.UserRemark,
          authority: self.UserAuthority,
        })
        .then(
          (response) => (
            this.$message("修改成功"),
            this.getUserContent(),
            this.CloseUserEdit()
          )
        )
        .catch(function (error) {
          alert("数据发送失败");
        });
    },
    UserEdit: function (UI, UN, UR, UA, show) {
      (this.UserId = UI),
        (this.UserName = UN),
        (this.UserRemark = UR),
        (this.UserAuthority = UA),
        (this.showModal = show);
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
    descInput: function () {
      this.txtVal = this.desc.length;
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
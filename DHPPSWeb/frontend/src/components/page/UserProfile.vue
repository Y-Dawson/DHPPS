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
                    query: { uI: this.AdminUserId },
                  }"
                  ><i class="ri-file-edit-line"></i
                  ><span>修改资料</span></router-link
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/',
                    query: { uI: this.AdminUserId },
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
                    :src="Url"
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
            <div class="col-lg-6" style="left:25%">
              <div class="iq-edit-list-data">
                <div class="tab-content">
                  <div
                    class="tab-pane fade active show"
                    id="personal-information"
                    role="tabpanel"
                  >
                    <div class="iq-card">
                      <div
                        class="iq-card-body"
                      >
                        <div class="imf">
                          <ul
                            id="todo-task1"
                            class="sub-task show mt-2 p-0"
                            style="list-style-type: none;"
                          >
                          <li>
                            <!-- <div class="demo-fit"> -->
                              <div class="block" v-for="fit in fits" :key="fit" style="text-align:center">
                                <el-avatar
                                  shape="circle"
                                  :size="70"
                                  :fit="fit"
                                  :src="Url"
                                ></el-avatar>
                              </div>
                            <!-- </div> -->
                          </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                                <i class="ri-checkbox-blank-circle-fill text-success"></i>
                              <span style="font-size:18px">
                                昵称： {{ MyContent.userName }}
                              </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                              <i
                                class="ri-checkbox-blank-circle-fill text-warning"
                              ></i>
                              <span style="font-size:18px">
                              性别： {{ MyContent.sex }}
                              </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                              <i
                                class="ri-checkbox-blank-circle-fill text-danger"
                              ></i>
                              <span style="font-size:18px">
                              生日： {{ MyContent.birth }}
                              </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                              <i
                                class="ri-checkbox-blank-circle-fill text-primary"
                              ></i><span style="font-size:18px">
                              手机号： {{ MyContent.phoneNumber }}
                              </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                              <i
                                class="ri-checkbox-blank-circle-fill text-info
"
                              ></i>
                              <span style="font-size:18px">
                              邮箱 {{ MyContent.email }}
                              </span>
                              </h5>
                            </li>
                            <li style="margin-top: 20px;margin-left:30%">
                              <h5>
                              <i
                                class="ri-checkbox-blank-circle-fill text-dark"
                              ></i>
                              <span style="font-size:18px">
                              住址 {{ MyContent.address }}
                              </span>
                              </h5>
                            </li>
                            <button style="margin-top: 40px" type="button" class="btn btn-primary btn-block">注销</button>
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
      // 头像
      fits: ["fill"],
      Url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      MyContent: [],
      AdminId: "25",
    };
  },
  created: function () {
    this.getMyContent(), this.getUserContent();
  },
  methods: {
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/25/")
        .then(
          (response) => (
            (self.MyContent = response.data),
            (this.Url = self.MyContent.avatar)
            // alert(JSON.stringify(self.MyContent))
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
  },
};
</script>

<style>
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
</style>
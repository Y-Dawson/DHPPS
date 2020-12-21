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
                    path: '/UserProfile',
                    query: { uI: this.AdminUserId },
                  }"
                  ><i class="ri-profile-line"></i
                  ><span>个人资料</span></router-link
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
              <li class="active">
                <a class="iq-waves-effect">
                <i class="ri-file-list-line"></i
                  ><span>我的案例</span></a>
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
                <div
                  class="box-card-group"
                  style="
                    margin-left: 60px;
                    margin-top: 20px;
                    width: auto;
                    height: 450px;
                    text-align: left;
                  ">
                  <el-col>
                    <!-- <el-card class="box-card">
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
                            @click="Edit(item.caseid)"
                            >进入编辑</el-button
                          >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: rgb(221, 0, 0)"
                            @click="Open(item.caseid)"
                            >删除</el-button
                          >
                        </div>
                      </div>
                      <dl class="box-text">
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
                      </dl>
                    </el-card> -->
                  </el-col>
                </div>
                <div class="paginate">
                  <button class="primaryb" @click="GetPrevPage()">上一页</button>
                  <span>第{{ currentPage }}页/共{{ totalPage }}页</span>
                  <button class="primaryb" @click="GetNextPage()">下一页</button>
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
      contentList: [],
      cases: [],
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 6, // 每页显示数量
      currentPageData: [], //当前页显示内容
    };
  },
  created: function () {
    this.getMyContent(), 
    this.getUserContent();
  },
  mounted: function () {
    this.GetCaseContent();
    this.SetPages();
  },
  methods: {
    //上一页
    GetPrevPage() {
      if (this.currentPage == 1) return;
      this.currentPage--;
      this.GetCaseContent();
    },
    // 下一页
    GetNextPage() {
      if (this.currentPage == this.totalPage) return;
      this.currentPage++;
      this.GetCaseContent();
    },
    SetPages() {
      if (this.totalPage < 1) totalPage = 1;
    },
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
    //获取案例内容
    GetCaseContent: function () {
      var self = this;
      axios
        .get("/apis/backend/case/", {
          params: {
            userId: 25,
            pageSize: 6,
            page: self.currentPage,
          },
        })
        .then(
          (response) => (
            (self.currentPageData = response.data),
            (self.totalPage = Math.ceil(
              self.currentPageData.pagination / self.pageSize
            ))
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert('数据请求失败')
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
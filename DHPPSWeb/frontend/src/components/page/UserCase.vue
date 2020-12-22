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
          <div style="text-align:center;">
                <div
                  class="box-card-group"
                  style="
                    margin-left: 60px;
                    margin-top: 20px;
                    width: auto;
                    height: 450px;
                    text-align: left;
                  ">
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
                        <span id="returnContent">{{ item.caseName }}</span>
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
                            @click="Edit(item.caseId)"
                            >进入编辑</el-button
                          >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: rgb(221, 0, 0)"
                            @click="Open(item.caseId)"
                            >删除</el-button
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
      totalCasePage: 1, // 统共页数，默认为1
      currentCasePage: 1, //当前页数 ，默认为1
      pageCaseSize: 6, // 每页显示数量
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
      if (this.totalCasePage < 1) totalCasePage = 1;
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/1/")
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
            userId: 1,
            pageSize: 6,
            page: self.currentCasePage,
          },
        })
        .then(
          (response) => (
            (self.currentPageData = response.data),
            (self.totalCasePage = Math.ceil(
              self.currentPageData.pagination / self.pageCaseSize
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
<style scoped>
.list {
  text-align: center;
  margin: 10px 300px;
}
.paginate {
  margin-top: 20px;
  /* margin-left: 200px; */
  /* left:50% */
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

</style>
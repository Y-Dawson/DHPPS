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
                    query: { uI: this.userId },
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
                    query: { uI: this.userId },
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
          <nav class="navbar navbar-expand-lg navbar-light p-0">
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
              <ul class="navbar-nav ml-auto navbar-list">
                <li class="nav-item"></li>
              </ul>
            </div>
            <ul class="navbar-list">
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
                  <img :src="imageUrl" class="img-fluid rounded mr-3" alt="user" />
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
                    margin-left: 100px;
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
                        <i
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
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 14px; color: #55587e"
                            @click="Edit(item.caseId)"
                            >进入编辑</el-button
                          >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 14px; color: rgb(221, 0, 0)"
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
      userId:'',
      // 头像
      fits: ["fill"],
      imageUrl:"",
      MyContent: [],
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
    this.GetUserIdentity()
    this.getMyContent()
  },
  mounted: function () {
    this.GetCaseContent();
    this.SetPages();
  },
  methods: {
    //获取用户身份
    GetUserIdentity(){
      var self=this
      axios
        .post("/apis/backend/getIdentity/")
        .then(response => (
           self.userId=response.data.userId
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
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
      if (this.totalCasePage < 1) totalCasePage = 1;
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/"+this.userId+"/")
        .then(
          (response) => (
            (self.MyContent = response.data[0]),
            (this.imageUrl = self.MyContent.avatar)
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
            userId: this.userId,
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
    // 案例编辑
    Edit: function (id) {
      var self = this;
      let data = new FormData();
      data.append("caseId", id);
      alert(id)
      axios
        .post("apis/backend/getCaseInfo/", data)
        .then((response) => {
          self.cases = response.data.cases;
          alert(JSON.stringify(self.cases)),
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
                userId: 1,
                caseName: this.cases.casename,
                citynum: this.cases.citynum,
                roadnum: this.cases.roadnum,
                InitCityData: city_inf,
                InitRoadData: road_inf,
                CityPosition: city_pos,
              }),
            },
          });
        })
        .catch(function (error) {
          alert(JSON.stringify(error.response));
          alert("数据请求失败wdnmd");
        });
    },
    DeleteCaseContent: function (id) {
      var self = this;
      // alert(id);
      axios
        .delete("apis/backend/case/" + id+ "/")
        .then(
          (response) => (self.currentPageData = response.data)
        )
        .catch(function (error) {
          alert('数据fas失败')
        });
    },
    Open(id) {
      this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.DeleteCaseContent(id),
            this.GetCaseContent(),
            // this.reload(),
            this.$message({
              type: "success",
              message: "删除成功!",
            });
          this.GetCaseContent();
        })
        .catch(() => {
          // this.$message({
          //   type: "info",
          //   message: "已取消删除",
          // });
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
.container-fluid{
  height:550px;
  padding: 0px;
}
.list {
  text-align: center;
  margin: 10px 300px;
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
  width: 300px;
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
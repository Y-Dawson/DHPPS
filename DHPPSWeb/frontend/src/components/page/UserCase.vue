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
                    margin-left: 40px;
                    margin-top: 20px;
                    margin-bottom:10px;
                    width: auto;
                    height: 480px;
                    text-align: left;
                  ">
                  <el-col
                    :span="8"
                    v-for="(item, index) in currentPageData.data"
                    :key="index"
                  >
                    <el-card class="box-card">
                      <div slot="header" class="clearfix">
                        <i v-if="item.caseMode === 1"
                          class="el-icon el-icon-location-outline"
                          style="
                            margin-right: 2px;
                            font-size: 38px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <i v-else-if="item.caseMode === 2"
                          class="el-icon el-icon-map-location"
                          style="
                            margin-right: 2px;
                            font-size: 38px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <span id="returnContent" style="font-size:16px;">{{ item.caseName }}</span>
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
      value:new Date(),
      userId:'',
      //判断是否已登录状态
      ifLogin:"",
      // 头像
      fits: ["fill"],
      imageUrl:"",
      MyContent: [],
      contentList: [],
      cases: [],
      caseMode:1,
      //分页
      restCase:0,
      totalCasePage: 1, // 统共页数，默认为1
      currentCasePage: 1, //当前页数 ，默认为1
      pageCaseSize: 6, // 每页显示数量
      currentPageData: [], //当前页显示内容
    };
  },
  created: function () {
    this.GetUserIdentity()
  },
  methods: {
    Show(){
      if(this.ifLogin=="返回数据成功"){
        this.getMyContent()
      }
      else{
        this.$message("你尚未登录")
        this.$router.push({
              path:'/Login'
          });
      }
    },
    //获取用户身份
    GetUserIdentity(){
      var self=this
      axios
        .post("/apis/backend/getIdentity/")
        .then(response => (
           self.userId=response.data.userId,
           self.ifLogin=response.data.message,
           this.Show()
          )
        )
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
    },
    GetFirstPage(){
      this.currentCasePage=1
      this.GetCaseContent()
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
      if(this.restCase>0){
        this.totalCasePage=this.totalCasePage+1;
      }
      if(this.currentPageData.pagination==0){
        this.totalCasePage=1;
      }
      // alert(this.totalCasePage)
      // if (this.totalCasePage < 1) totalCasePage = 1;
    },
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/"+this.userId+"/")
        .then(
          (response) => (
            self.MyContent = response.data,
            this.imageUrl = self.MyContent.avatarUrl,
            this.GetCaseContent()
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
            self.currentPageData = response.data,
            // alert(response.data),
            self.totalCasePage = Math.floor(
              self.currentPageData.pagination / self.pageCaseSize
            ),
            self.restCase=self.currentPageData.pagination-(self.totalCasePage*self.pageCaseSize),
            this.SetPages()
          )
        )
        .catch(function (error) {
          // 请求失败处理
          // alert('数据请求失败了')
          this.GetCaseContent()
        });
    },
    // 案例编辑
    Edit: function (id) {
      var self = this;
      let data = new FormData();
      data.append("caseId", id);
      axios
        .post("/apis/backend/getCaseInfo/", data)
        .then((response) => {
          self.cases = response.data.cases;
          // alert(JSON.stringify(self.cases)),
          // console.log(JSON.stringify(self.cases));
          self.caseMode=self.cases.caseMode
          // console.log(self.cases.InitCityData);
          var city_inf = [];
          for (var j in self.cases.InitCityData) {
            var s =
              "cityname:" +
              self.cases.InitCityData[j].cityName +
              ",initpop:" +
              self.cases.InitCityData[j].initPop +
              ",initinfect:" +
              self.cases.InitCityData[j].initInfect;
            console.log("s:", s);
            city_inf.push(s);
          }

          var road_inf = [];
          for (var j in self.cases.InitRoadData) {
            var s =
              "departure:" +
              self.cases.InitRoadData[j].departure +
              ",destination:" +
              self.cases.InitRoadData[j].destination +
              ",volume:" +
              self.cases.InitRoadData[j].volume;
            console.log("s:", s);
            road_inf.push(s);
          }

          var city_pos = [];
          for (var j in self.cases.CityPosition) {
            var s =
              "cityname:" +
              self.cases.CityPosition[j].cityName +
              ",x:" +
              self.cases.CityPosition[j].x +
              ",y:" +
              self.cases.CityPosition[j].y;
            console.log("s:", s);
            city_pos.push(s);
          }
          if(this.caseMode== 1){
            this.$router.push({
            path: "/setting",
            query: {
              params: JSON.stringify({
                userId: this.userId,
                caseName: this.cases.casename,
                citynum: this.cases.citynum,
                roadnum: this.cases.roadnum,
                InitCityData: city_inf,
                InitRoadData: road_inf,
                CityPosition: city_pos,
              }),
            },
          });
          }
          else if(this.caseMode== 2){
            // alert(this.caseMode)
            this.$router.push({
            path: "/settingMap",
            query: {
              params: JSON.stringify({
                userId: this.userId,
                caseName: this.cases.casename,
                citynum: this.cases.citynum,
                roadnum: this.cases.roadnum,
                InitCityData: city_inf,
                InitRoadData: road_inf,
                CityPosition: city_pos,
              }),
            },
          });
          }
          
        })
        .catch(function (error) {
          alert(JSON.stringify(error.response));
          alert("getCaseInfo数据请求失败wdnmd");
        });
    },
    DelayReload:function(){
      setTimeout(function(){  //使用  setTimeout（）方法设bai定定时du1000毫秒
      window.location.reload();//页面刷新zhi
    },200)
    },
    DeleteCaseContent: function (id) {
      var self = this;
      // alert(id);
      axios
        .delete("/apis/backend/case/" + id+ "/")
        .then((response) => (
          self.currentPageData = response.data,
          this.GetCaseContent(),
          this.$message({
              type: "success",
              message: "删除成功!",
          }),
          this.GetFirstPage()
          // this.DelayReload()
        ))
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
          this.DeleteCaseContent(id)
          this.GetCaseContent()
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
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
  width: 280px;
  /* float: left; */
  margin-right: 40px;
  margin-left: 10px;
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
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
                  ><i class="ri-home-4-line"></i><span>首页</span></a
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
                    query: { uI: this.AdminId },
                  }"
                  ><i class="ri-user-line"></i
                  ><span>信息管理</span></router-link
                >
              </li>
              <li>
                <router-link
                  class="iq-waves-effect"
                  :to="{
                    path: '/AdminCaseManage',
                    query: { uI: this.AdminId },
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
      <div id="content-page" class="content-page">
        <div class="container-fluid">
          <div class="row">
            <div class="col-sm-2 col-lg-5">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">城市喜爱度</h4>
                  </div>
                </div>
                <div class="iq-card-body">
                  <ve-ring
                    :data="chartCityData"
                    :extend="chartCityExtend"
                    :settings="chartCitySettings"
                    height="250px"
                  >
                  </ve-ring>
                </div>
              </div>

              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">性别比例图</h4>
                  </div>
                </div>
                <div class="iq-card-body">
                  <ve-ring
                    :data="chartRingData"
                    :extend="chartRingExtend"
                    :settings="chartRingSettings"
                    height="200px"
                  >
                  </ve-ring>
                </div>
              </div>
            </div>
            <div class="col-sm-10 col-lg-7">
              <div class="iq-card">
                <div class="iq-card-header d-flex justify-content-between">
                  <div class="iq-header-title">
                    <h4 class="card-title">数据</h4>
                  </div>
                </div>
                <div class="iq-card-body">
                  <ve-histogram :data="chartHistogramData" 
                    height="500px" ></ve-histogram>
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
<script src="https://www.jq22.com/jquery/jquery-1.10.2.js"></script>
<script>
import VeRing from "v-charts/lib/ring.common";
import VeHistogram from 'v-charts/lib/histogram.common';
export default {
  components: {
    [VeRing.name]: VeRing,
    [VeHistogram.name]: VeHistogram,
  },
  data() {
    this.chartRingExtend = {
      legend: { show: false }, //隐藏legend
      series: {
        center: ["50%", "50%"],
      },
    };
    this.chartCityExtend = {
      legend: { show: false }, //隐藏legend
      series: {
        center: ["50%", "50%"],
      },
    };
    return {
      // 头像
      fits: ["fill"],
      AdminUrl: "",
      MyContent: [],
      AdminId: "25",
      sexData:[],
      cityData: [],
      chartRingData: {
        columns: ["性别", "用户数量"],
        rows: [],
      },
      chartCityData: {
        columns: ["城市", "使用数量"],
        rows: [],
      },
      chartHistogramData: {
          columns: ['日期', '用户数量', '案例数量', ],
          rows: [
            { '日期': '2020.09', '用户数量': 1393, '案例数量': 1093, },
            { '日期': '2020.10', '用户数量': 3530, '案例数量': 3230, },
            { '日期': '2020.11', '用户数量': 3981, '案例数量': 4281, },
            { '日期': '2020.12', '用户数量': 4233, '案例数量': 5212, },
            { '日期': '2021.01', '用户数量': 5124, '案例数量': 6712, }
          ]
        },
      chartRingSettings: {
        radius: ["60px", "80px"],
        itemStyle: {
          //这里是更添加阴影
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
          //这里是更改颜色
          normal: {
            color: function (params) {
              var colorList = [
                "rgb(90,177,239)",
                "rgb(25,212,174)",
                "rgb(130,122,243)",
              ];
              return colorList[params.dataIndex];
            },
          },
        },
      },chartCitySettings: {
        radius: ["60px", "80px"],
        itemStyle: {
          //这里是更添加阴影
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
          //这里是更改颜色
          normal: {
            color: function (params) {
              var colorList = [
                "rgb(90,177,239)",
                "rgb(251,198,71)",
                "rgb(25,212,174)",
                "rgb(108,230,244)",
                "rgb(130,122,243)",
                "rgb(200,200,200)",
              ];
              return colorList[params.dataIndex];
            },
          },
        },
      },
    };
  },
  created: function () {
    this.getMyContent();
    this.getSexData();
    this.getCityData();
  },
  methods: {
    getMyContent: function () {
      var self = this;
      axios
        .get("/apis/backend/profile/25/")
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
    getSexData: function() {
      var self = this;
      axios
        .get("/apis/backend/sexNum/")
        .then(
          (response) => {
            alert(JSON.stringify(response.data.TopcityInfos))
          this.sexData = response.data.TopcityInfos;
          //通过遍历DataShow分别给columns 中的维度和指标 赋值；
          for (var i = 0; i < this.sexData.length; i++) {
            this.chartRingData.rows.push({
         //注意，由于我后端createTime该字段直接返回是一个时间戳，所以此处用到了 一个时间转换插件moment.js
              "性别": this.sexData[i].sex,
              "用户数量": this.sexData[i].sexCount,
            });

          }
          }
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    getCityData:function(){
      var self = this;
      axios
        .get("/apis/backend/topCity/")
        .then(
          (response) => {
            alert(JSON.stringify(response.data))
          this.cityData = response.data;
          //通过遍历DataShow分别给columns 中的维度和指标 赋值；
          for (var i = 0; i < this.sexData.length; i++) {
            this.chartRingData.rows.push({
         //注意，由于我后端createTime该字段直接返回是一个时间戳，所以此处用到了 一个时间转换插件moment.js
              "城市": this.sexData[i].sex,
              "使用数量": this.sexData[i].sexCount,
            });

          }
          }
        )
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    }
  },
};
</script>

<style scoped>
@import "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css";
@import "../../css/bootstrap.min.css";
@import "../../css/typography.css";
@import "../../css/style.css";
@import "../../css/animate.css";
/* @import "../../images/favicon.ico"; */
@import "../../css/style.css";
.avatar-md img {
  width: 38px;
}
.rounded-circle {
  border-radius: 50% !important;
}
</style>
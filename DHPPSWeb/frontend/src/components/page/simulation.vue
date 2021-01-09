<template>
  <div id="simulation">
    <!-- <div class="layui-layout layui-layout-admin">
      <div class="layui-header">
        <div class="layui-logo">LOGO</div>
        <div class="layui-logotext">高传染性疾病预测系统</div>
        <ul class="layui-nav layui-layout-right">
          <li class="layui-nav-item" style="line-height: 20px">
            <el-avatar shape="circle" :size="30" :fit="fit" :src="url"></el-avatar>
          </li>
          <li class="layui-nav-item">
            <a href="javascript:;">
              <span>用户名</span>
            </a>
          </li>
        </ul>
      </div>
    </div> -->
    <header>
      <h1>数据可视化</h1>
    </header>

    <canvas
      id="myCanvas"
      width="1320"
      height="660"
      style="border: 1px solid #c3c3c3"
      ref="canvas"
    ></canvas>

    <el-form ref="cityFormRef" :model="cityForm" :rules="cityFormRule">
      <ul class="tools-wrapper">
        <li>
          <el-form-item class="new-pointer">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-add-circle"></i>
              <span>新建节点</span>
            </el-button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="connect-pointer">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-release"></i>
              <span>连接节点</span>
            </el-button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="delete-pointer">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-delete"></i>
              <span>删除节点</span>
            </el-button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="delete-road">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-fonts-clear"></i>
              <span>删除道路</span>
            </el-button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="stop-simulate">
            <button
              type="primary"
              v-bind:class="{ active1: ss }"
              @click="
                ss = !ss;
                StopSimulation(ss);
              "
            >
              <i class="layui-icon layui-icon-pause"></i>
              <span>停止模拟</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="save-case">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-log"></i>
              <span>保存案例</span>
            </el-button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="my-case">
            <el-button type="primary" disabled>
              <i class="layui-icon layui-icon-user"></i>
              <span>我的案例</span>
            </el-button>
          </el-form-item>
        </li>
      </ul>

      <!-- <div class="add-wrapper">
        <i class="layui-icon layui-icon-add-1 add">
          <ul class="tools-list">
            <li>
              <button class="examples">
                <i class="layui-icon layui-icon-template-1"></i>
                <span>示例</span>
              </button>
            </li>
            <li>
              <button class="visualization">
                <i class="layui-icon layui-icon-chart"></i>
                <span>模型可视化</span>
              </button>
            </li>
            <li>
              <button class="change-password">
                <i class="layui-icon layui-icon-password"></i>
                <span>修改密码</span>
              </button>
            </li>
            <li>
              <button class="cancellation">
                <i class="layui-icon layui-icon-return"></i>
                <span>注销</span>
              </button>
            </li>
          </ul>
        </i>
      </div> -->

      <ul class="city-list">
        <li style="margin-bottom: 20px">
          <div class="panel">
            <h2>城市信息</h2>
            <div class="chart" id="bar"></div>
            <!-- <span class="little-title">城市列表：</span>
            <li id="city_inf" v-for="city in city_inf" :key="city">
              {{ city[day] }}
            </li> -->
          </div>
        </li>
        <li>
          <div class="panel">
            <h2>道路信息</h2>
            <div class="chart" id="threebar"></div>
            <!-- <span class="little-title">道路列表：</span>
            <li id="road_inf" v-for="road in road_di" :key="road">
              {{ road }}
            </li> -->
          </div>
        </li>
      </ul>

      <ul class="img-list">
        <li v-for="o in citycnt + 20" :key="o">
          <div :id="'ci' + o" class="city" style="left: 10000px; top: 10000px">
            <img
              src="../../assets/layui/images/city.gif"
              alt=""
              :title="cityname[o-1]"
              @click="outp('cityinf' + o)"
            />
            <div class="city-infor" :id="'cityinf' + o">
              <div v-for="j in row_cnt[o]" :key="j">
                <span v-for="k in people_cnt[o][j]" :key="k" class="text item">
                  <i
                    :id="'i' + o + j + k"
                    class="el-icon-user-solid"
                  ></i>
                </span>
              </div>
            </div>
          </div>
        </li>
      </ul>

      <ul class="line_list">
        <li v-for="o in initline + 50" :key="o">
          <div
            :id="'line' + o"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
            @click="DeleteRoad('line' + o)"
          >
            <img src="../../assets/img/road_line.png" alt="" />
            <span></span>
            <span></span>
          </div>
        </li>
      </ul>

      <div class="block">
        <el-slider
          v-model="value1"
          :format-tooltip="FormatTooltip"
          :step="daily_step"
          show-stops
        ></el-slider>
      </div>
    </el-form>
  </div>
</template>

<script src="http://g.tbcdn.cn/mtb/lib-flexible/0.3.4/??flexible_css.js,flexible.js"></script>
<script>
import Global from "../../global_vue";
import { jquery } from "../../assets/js/jquery.js";
var echarts = require("echarts");
import "../../../node_modules/echarts/lib/chart/map/china.js";

var linecnt = 1;

export default {
  data() {
    return {
      fits: ["fill"],
      url: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",

      ss: false,
      disable: true,
      value1: 0,
      daily_step: 0,
      day_num: 0,

      initline: 0,

      cityx1: 0,
      cityy1: 0,
      cityx2: 0,
      cityy2: 0,

      isdisabled1: false,
      isdisabled2: false,
      isdisabled3: false,
      showed: true,
      // cityleft: Global.cityleft,
      // citytop: Global.citytop,
      lineleft: Global.lineleft,
      linetop: Global.linetop,
      params: "",

      cityForm: {
        // cityName: "",
        population: "",
        beginInfected: "",
        distance: "",
        traffic: "",
        cityleft: Global.cityleft,
        citytop: Global.citytop,
      },

      day: 0,

      userId: "",
      casename: "",
      citycnt: 100,
      linecnt: 100,

      people_cnt: [[]],
      row_cnt: [],

      city_inf: [],
      city_information: [], //初始信息
      road_inf: [],
      city_position: [],
      name_list: ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],

      ci1_population: [],
      ci1_totalInfected: [],
      ci1_newInfected: [],
      ci2_population: [],
      ci2_totalInfected: [],
      ci2_newInfected: [],
      ci3_population: [],
      ci3_totalInfected: [],
      ci3_newInfected: [],
      ci4_population: [],
      ci4_totalInfected: [],
      ci4_newInfected: [],
      ci5_population: [],
      ci5_totalInfected: [],
      ci5_newInfected: [],
      ci6_population: [],
      ci6_totalInfected: [],
      ci6_newInfected: [],
      ci7_population: [],
      ci7_totalInfected: [],
      ci7_newInfected: [],
      ci8_population: [],
      ci8_totalInfected: [],
      ci8_newInfected: [],
      ci9_population: [],
      ci9_totalInfected: [],
      ci9_newInfected: [],
      ci10_population: [],
      ci10_totalInfected: [],
      ci10_newInfected: [],

      cityname: [],
      citypeople: [],
      cityInf: [],
      cityNewInf: [],
      roadVol: [],

      city_po: [],
      road_di: [],
      road_c1: "",
      road_c2: "",
      ci: ["ci1", "ci2", "ci3", "ci4", "ci5", "ci6", "ci7", "ci8", "ci9", "ci10"],
      ri: [
        "line1",
        "line2",
        "line3",
        "line4",
        "line5",
        "line6",
        "line7",
        "line8",
        "line9",
        "line10",
        "line11",
        "line12",
      ],
      cityFormRule: {
        population: [
          { required: true, message: "请输入城市人数", trigger: "blur" },
          {
            min: 1,
            max: 15000,
            message: "城市人数在0到15000之间",
            trigger: "blur",
          },
        ],
        beginInfected: [
          {
            required: true,
            message: "请输入城市初始感染人数",
            trigger: "blur",
          },
          {
            min: 0,
            max: 100,
            message: "城市初始感染人数在0到100之间",
            trigger: "blur",
          },
        ],
        traffic: [
          {
            required: true,
            message: "请输入此道路的人流量",
            trigger: "blur",
          },
          {
            min: 0,
            max: 1000,
            message: "人流量在0到1000之间",
            trigger: "blur",
          },
        ],
      },
    };
  },

  mounted: function () {
    this.GetUserIdentity();

    this.params = JSON.parse(this.$route.query.params);

    // console.log("用户ID：", this.params.userId);
    // console.log("案例名：", this.params.caseName);
    // console.log("城市数目：", this.params.citynum);
    // console.log("道路数目：", this.params.roadnum);
    // console.log("初始城市信息：", this.params.InitCityData);
    // console.log("道路信息：", this.params.InitRoadData);
    // console.log("城市坐标：", this.params.CityPosition);
    // console.log("每日病例：", this.params.DailyInfected.data.DailyForecastData);
    var foreData = this.params.DailyInfected.data.DailyForecastData;

    // this.userId = this.params.userId;
    this.casename = this.params.caseName;
    this.citycnt = this.params.citynum;
    this.linecnt = this.params.roadnum;
    this.city_information = this.params.InitCityData;
    this.road_inf = this.params.InitRoadData;
    this.city_position = this.params.CityPosition;
    this.day_num = parseInt(this.params.Daynum);
    this.daily_step = 100 / this.day_num;
    // console.log("模拟天数：", this.params.Daynum);
    // console.log("每日跨度：", this.daily_step);

    for (var i = 0; i < parseInt(this.params.Daynum) + 1; i++) {
      for (var j = 0; j < parseInt(this.params.citynum); j++) {
        this.AddInformation(
          foreData[i][j]["cityName"],
          foreData[i][j]["population"],
          foreData[i][j]["dailyinfected"],
          foreData[i][j]["infected"]
        );
      }
    }

    // console.log("录入病例信息完毕");

    for (var i = 0; i < parseInt(this.params.citynum); i++) {
      this.cityname.push(foreData[0][i]["cityName"]);
    }

    for (var i = 0; i < parseInt(this.params.citynum); i++) {
      var newa = new Array();
      for (var j = 0; j < parseInt(this.params.Daynum); j++) {
        var s =
          foreData[j][i]["cityName"] +
          ":" +
          foreData[j][i]["population"] +
          "," +
          foreData[j][i]["dailyinfected"] +
          "," +
          foreData[j][i]["infected"];
        newa.push(s);
      }
      this.city_inf.push(newa);
    }

    // console.log("录入病例显示信息完毕");

    this.row_cnt.push(1);

    // console.log("citynum", this.citycnt);
    // console.log("c3inf", this.ci3_totalInfected);

    var nowcitycnt = 0;
    for (var i = 0; i < parseInt(this.params.citynum); i++) {
      if (foreData[0][i]["cityName"] != this.name_list[nowcitycnt]) {
        nowcitycnt += 1;
        this.row_cnt.push(1);
        this.people_cnt.push(1);
        // console.log("i", i);
        // console.log("name", foreData[0][i]["cityName"]);
        i -= 1;
        continue;
      }
      nowcitycnt += 1;
      var pop = parseInt(foreData[0][i]["population"]);
      pop = parseInt(pop / 100);
      var temp = parseInt(pop / 10);
      if (pop % 10 != 0) {
        temp += 1;
      }
      this.row_cnt.push(temp);
      var newb = new Array();
      newb.push(1);
      for (var j = 1; j <= temp; j++) {
        if (j < temp) {
          newb.push(10);
        } else {
          var le = pop - (temp - 1) * 10;
          newb.push(le);
        }
      }
      this.people_cnt.push(newb);
    }

    this.row_cnt.push(0);
    // console.log("rc", this.row_cnt);
    // console.log("pc", this.people_cnt);

    var cnt = 0;
    for (var j in this.params.CityPosition) {
      var te = this.params.CityPosition[j].split(",");
      // console.log("te", te);
      // console.log("j", j);
      var tt, ci, x, y, cid;
      cnt = 0;
      for (var k in te) {
        cnt++;
        if (cnt == 1) {
          tt = te[k].split(":");
          ci = tt[1];
        }
        if (cnt == 2) {
          tt = te[k].split(":");
          x = tt[1];
        }
        if (cnt == 3) {
          tt = te[k].split(":");
          y = tt[1];
        }
      }
      cid = this.GetID(ci);
      var cityentity = document.getElementById(cid);

      // console.log("cityID", cid);
      // console.log("cityentity", cityentity);

      cityentity.style.left = x + "px";
      cityentity.style.top = y + "px";
      cityentity.style.display = "block";

      this.changePosition(ci);

      // console.log("x", x);
      // console.log("y", y);

      // console.log("cityID", cid);
    }

    for (var j in this.params.InitRoadData) {
      // console.log(this.params.InitRoadData[j]);
      var ri = this.params.InitRoadData[j].split(",");
      // console.log(ri);
      var city1, city2, vol, tt, s;
      cnt = 0;
      for (var k in ri) {
        cnt += 1;
        if (cnt == 1) {
          tt = ri[k].split(":");
          city1 = tt[1];
        }
        if (cnt == 2) {
          tt = ri[k].split(":");
          city2 = tt[1];
        }
        if (cnt == 3) {
          tt = ri[k].split(":");
          vol = tt[1];
        }
      }
      s = city1 + "-" + city2 + ":" + vol;
      this.road_di.push(s);
      var cid1 = this.GetID(city1);
      var cid2 = this.GetID(city2);
      // console.log(cid1, cid2);

      var newar1 = new Array();
      newar1.push(city1);
      newar1.push(city2);
      newar1.push(vol);
      this.roadVol.push(newar1);

      var newar2 = new Array();
      newar2.push(city2);
      newar2.push(city1);
      newar2.push(vol);
      this.roadVol.push(newar2);

      this.DrawLine(cid1, cid2);
    }

    // console.log("c1_inf：", this.ci1_population);

    this.DrawRoadMap();
  },

  methods: {
    GetUserIdentity() {
      axios
        .post("/apis/backend/getIdentity/")
        .then((response) => {
          this.userId = response.data.userId;
          if (response.data.message != "返回数据成功") {
            this.$message("您尚未登录");
            this.$router.push({
              path:'/Login'
            })
          }
          // alert(JSON.stringify(response.data)),
        })
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
    },

    StopSimulation(ss) {
      if (this.ss == true) {
        // console.log("返回设置参数界面");
        this.ss = false;
        this.$router.push({
          path: "/setting",
          query: {
            params: JSON.stringify({
              caseName: this.casename,
              citynum: this.citycnt,
              roadnum: this.linecnt,
              InitCityData: this.city_information,
              InitRoadData: this.road_inf,
              CityPosition: this.city_position,
            }),
          },
        });
      }
    },

    FormatTooltip(val) {
      this.day = parseInt(val / this.daily_step);
      // console.log("day：", this.day);
      this.changeColor(this.day);
      this.prepareDraw(this.day);
      var d = parseInt(val / this.daily_step) + 1;
      var m = 1;
      if (d > 31) {
        m += 1;
        d -= 31;
      }
      if (d > 28) {
        m += 1;
        d -= 28;
      }
      if (d > 31) {
        m += 1;
        d -= 31;
      }
      if (d > 30) {
        m += 1;
        d -= 30;
      }
      var s = m + "月" + d + "日";
      return s;
    },

    DrawLine(ci1, ci2) {
      // console.log("画条线");
      var c1 = document.getElementById(ci1);
      var c2 = document.getElementById(ci2);

      var cx1 = c1.style.left;
      var tcx1 = cx1.substring(0, cx1.length - 2);
      var cy1 = c1.style.top;
      var tcy1 = cy1.substring(0, cy1.length - 2);
      var cx2 = c2.style.left;
      var tcx2 = cx2.substring(0, cx2.length - 2);
      var cy2 = c2.style.top;
      var tcy2 = cy2.substring(0, cy2.length - 2);

      // console.log("tcx1:", tcx1);
      // console.log("tcy1:", tcy1);
      // console.log("tcx2:", tcx2);
      // console.log("tcy2:", tcy2);

      const dx = Math.abs(tcx1 - tcx2);
      const dy = Math.abs(tcy1 - tcy2);
      var dis = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

      // console.log("dis:", dis);

      var ttcx1 = parseInt(tcx1);
      var ttcx2 = parseInt(tcx2);
      var ttcy1 = parseInt(tcy1);
      var ttcy2 = parseInt(tcy2);

      var rotang = 0;
      if ((ttcx1 <= ttcx2 && ttcy1 <= ttcy2) || (ttcx1 >= ttcx2 && ttcy1 >= ttcy2)) {
        rotang = Math.asin(parseFloat(dy / dis));
        rotang = (rotang / Math.PI) * 180;
      }
      if ((ttcx1 <= ttcx2 && ttcy1 >= ttcy2) || (ttcx1 >= ttcx2 && ttcy1 <= ttcy2)) {
        rotang = Math.asin(parseFloat(dy / dis));
        rotang = (rotang / Math.PI) * 180;
        rotang = 180 - rotang;
      }

      var ll = document.getElementById("line" + linecnt);
      ll.style.left = (ttcx1 + ttcx2) / 2 - parseInt(dis) / 2 + 30 + "px";
      ll.style.top = (ttcy1 + ttcy2) / 2 + 100 + "px";
      ll.style.transition = "width 2s";
      ll.style.width = parseInt(dis) + "px";
      ll.style.transform = "rotate(" + rotang + "deg)";
      linecnt += 1;

      // console.log("ll",ll);
      // console.log("left",ll.style.left);
      // console.log("top",ll.style.top);
      // var ii=document.getElementById("img1");
      // ii.style.animation="roadmove1 3s infinite";

      // console.log("ii",ii);
      // console.log("ii.style",ii.style.animation);
    },

    GetID(n) {
      if (n == "A") return "ci1";
      if (n == "B") return "ci2";
      if (n == "C") return "ci3";
      if (n == "D") return "ci4";
      if (n == "E") return "ci5";
      if (n == "F") return "ci6";
      if (n == "G") return "ci7";
      if (n == "H") return "ci8";
      if (n == "I") return "ci9";
      if (n == "J") return "ci10";
      if (n == "K") return "ci11";
      if (n == "L") return "ci12";
    },

    GetNum(n) {
      if (n == "A") return 1;
      if (n == "B") return 2;
      if (n == "C") return 3;
      if (n == "D") return 4;
      if (n == "E") return 5;
      if (n == "F") return 6;
      if (n == "G") return 7;
      if (n == "H") return 8;
      if (n == "I") return 9;
      if (n == "J") return 10;
      if (n == "K") return 11;
      if (n == "L") return 12;
    },

    getCityName(n){
      if(n==1) return "A";
      if(n==2) return "B";
      if(n==3) return "C";
      if(n==4) return "D";
      if(n==5) return "E";
      if(n==6) return "F";
      if(n==7) return "G";
      if(n==8) return "H";
      if(n==9) return "I";
      if(n==10) return "J";
    },

    AddInformation(n, popu, dinf, inf) {
      if (n == "A") {
        this.ci1_population.push(popu);
        this.ci1_totalInfected.push(inf);
        this.ci1_newInfected.push(dinf);
      }
      if (n == "B") {
        this.ci2_population.push(popu);
        this.ci2_totalInfected.push(inf);
        this.ci2_newInfected.push(dinf);
      }
      if (n == "C") {
        this.ci3_population.push(popu);
        this.ci3_totalInfected.push(inf);
        this.ci3_newInfected.push(dinf);
      }
      if (n == "D") {
        this.ci4_population.push(popu);
        this.ci4_totalInfected.push(inf);
        this.ci4_newInfected.push(dinf);
      }
      if (n == "E") {
        this.ci5_population.push(popu);
        this.ci5_totalInfected.push(inf);
        this.ci5_newInfected.push(dinf);
      }
      if (n == "F") {
        this.ci6_population.push(popu);
        this.ci6_totalInfected.push(inf);
        this.ci6_newInfected.push(dinf);
      }
      if (n == "G") {
        this.ci7_population.push(popu);
        this.ci7_totalInfected.push(inf);
        this.ci7_newInfected.push(dinf);
      }
      if (n == "H") {
        this.ci8_population.push(popu);
        this.ci8_totalInfected.push(inf);
        this.ci8_newInfected.push(dinf);
      }
      if (n == "I") {
        this.ci9_population.push(popu);
        this.ci9_totalInfected.push(inf);
        this.ci9_newInfected.push(dinf);
      }
      if (n == "J") {
        this.ci10_population.push(popu);
        this.ci10_totalInfected.push(inf);
        this.ci10_newInfected.push(dinf);
      }
    },

    changeColor(index) {
      // console.log("动起来");
      // console.log(this.citycnt);
      var ccnt = 0;
      var nowcnt = 0;
      for (var i in this.cityname) {
        // console.log("row", this.row_cnt[i]);
        nowcnt += 1;
        ccnt = this.GetNum(this.cityname[i]);
        // console.log("ccnt", ccnt);
        // console.log("nowcnt", nowcnt);
        // console.log("typeofnowcnt", typeof nowcnt);
        // console.log("row_cnt", this.row_cnt);
        // console.log("row_cnt[nowcnt]", this.row_cnt[ccnt]);
        for (var j = 1; j <= this.row_cnt[ccnt]; j++) {
          if (j < this.row_cnt[ccnt]) {
            for (var k = 1; k <= 10; k++) {
              var iid = "i" + ccnt + j + k;
              // console.log("iid", iid);
              var iidentity = document.getElementById(iid);
              // console.log("iidentity", iidentity);
              iidentity.style.color = "green";
              // console.log("iid", iid);
            }
          } else {
            // console.log("换行");
            for (var k = 1; k <= this.people_cnt[ccnt][j]; k++) {
              var iid = "i" + ccnt + j + k;
              var iidentity = document.getElementById(iid);
              // console.log("iidentity", iidentity);
              iidentity.style.color = "green";
              // console.log("iid", iid);
            }
          }
        }

        var inf_cnt = 0;
        if (ccnt == 1) {
          inf_cnt = parseInt(this.ci1_totalInfected[index]);
        }
        if (ccnt == 2) {
          inf_cnt = parseInt(this.ci2_totalInfected[index]);
        }
        if (ccnt == 3) {
          inf_cnt = parseInt(this.ci3_totalInfected[index]);
        }
        if (ccnt == 4) {
          inf_cnt = parseInt(this.ci4_totalInfected[index]);
        }
        if (ccnt == 5) {
          inf_cnt = parseInt(this.ci5_totalInfected[index]);
        }
        if (ccnt == 6) {
          inf_cnt = parseInt(this.ci6_totalInfected[index]);
        }
        if (ccnt == 7) {
          inf_cnt = parseInt(this.ci7_totalInfected[index]);
        }
        if (ccnt == 8) {
          inf_cnt = parseInt(this.ci8_totalInfected[index]);
        }
        if (ccnt == 9) {
          inf_cnt = parseInt(this.ci9_totalInfected[index]);
        }
        if (ccnt == 10) {
          inf_cnt = parseInt(this.ci10_totalInfected[index]);
        }

        inf_cnt = parseInt(inf_cnt / 100);
        // console.log("tot", this.ci1_totalInfected[index]);
        // console.log("inf_cnt", inf_cnt);

        for (var j = 1; j <= this.row_cnt[ccnt]; j++) {
          if (inf_cnt > 10) {
            for (var k = 1; k <= 10; k++) {
              var iid = "i" + ccnt + j + k;
              var iidentity = document.getElementById(iid);
              // console.log("iidentity", iidentity);
              iidentity.style.color = "red";
            }
            inf_cnt -= 10;
          } else {
            for (var k = 1; k <= inf_cnt; k++) {
              var iid = "i" + ccnt + j + k;
              var iidentity = document.getElementById(iid);
              // console.log("iidentity", iidentity);
              iidentity.style.color = "red";
            }
            break;
          }
        }
      }
    },

    outp(e) {
      var cinf = document.getElementById(e);
      // console.log("cinf", cinf);
      if (cinf.style.display != "none") {
        cinf.style.display = "none";
      } else {
        cinf.style.display = "block";
      }
      // console.log("dis", cinf.style.display);
    },

    changePosition(e) {
      // console.log("改变位置");

      var cnum = this.GetNum(e);
      var cinf = "cityinf" + cnum;
      var cid = this.GetID(e);
      var ci = document.getElementById(cinf);
      var c = document.getElementById(cid);

      // console.log("cid", cid);

      ci.style.marginTop = -240 + "px";
      ci.style.marginLeft = 75 + "px";

      var ct = c.style.top;
      // console.log("ct", ct);
      var tct = parseInt(ct.substring(0, ct.length - 2));
      // console.log("tct", tct);
      if (tct < 150) {
        // console.log("你的top不对劲");
        ci.style.marginTop = -90 - tct + "px";
      }
    },

    prepareDraw(nowday) {
      this.citypeople = [];
      this.cityInf = [];
      this.cityNewInf = [];
      for (var i in this.cityname) {
        if (this.cityname[i] == "A") {
          this.citypeople.push(this.ci1_population[nowday]);
          this.cityInf.push(this.ci1_totalInfected[nowday]);
          this.cityNewInf.push(this.ci1_newInfected[nowday]);
        }
        if (this.cityname[i] == "B") {
          this.citypeople.push(this.ci2_population[nowday]);
          this.cityInf.push(this.ci2_totalInfected[nowday]);
          this.cityNewInf.push(this.ci2_newInfected[nowday]);
        }
        if (this.cityname[i] == "C") {
          this.citypeople.push(this.ci3_population[nowday]);
          this.cityInf.push(this.ci3_totalInfected[nowday]);
          this.cityNewInf.push(this.ci3_newInfected[nowday]);
        }
        if (this.cityname[i] == "D") {
          this.citypeople.push(this.ci4_population[nowday]);
          this.cityInf.push(this.ci4_totalInfected[nowday]);
          this.cityNewInf.push(this.ci4_newInfected[nowday]);
        }
        if (this.cityname[i] == "E") {
          this.citypeople.push(this.ci5_population[nowday]);
          this.cityInf.push(this.ci5_totalInfected[nowday]);
          this.cityNewInf.push(this.ci5_newInfected[nowday]);
        }
        if (this.cityname[i] == "F") {
          this.citypeople.push(this.ci6_population[nowday]);
          this.cityInf.push(this.ci6_totalInfected[nowday]);
          this.cityNewInf.push(this.ci6_newInfected[nowday]);
        }
        if (this.cityname[i] == "G") {
          this.citypeople.push(this.ci7_population[nowday]);
          this.cityInf.push(this.ci7_totalInfected[nowday]);
          this.cityNewInf.push(this.ci7_newInfected[nowday]);
        }
        if (this.cityname[i] == "H") {
          this.citypeople.push(this.ci8_population[nowday]);
          this.cityInf.push(this.ci8_totalInfected[nowday]);
          this.cityNewInf.push(this.ci8_newInfected[nowday]);
        }
        if (this.cityname[i] == "I") {
          this.citypeople.push(this.ci9_population[nowday]);
          this.cityInf.push(this.ci9_totalInfected[nowday]);
          this.cityNewInf.push(this.ci9_newInfected[nowday]);
        }
        if (this.cityname[i] == "J") {
          this.citypeople.push(this.ci10_population[nowday]);
          this.cityInf.push(this.ci10_totalInfected[nowday]);
          this.cityNewInf.push(this.ci10_newInfected[nowday]);
        }
      }

      this.DrawMap();
    },

    DrawMap() {
      // console.log("画个柱状图");

      var myChart = echarts.init(document.getElementById("bar"));

      var seriesLabel = {
        normal: {
          show: true,
          textBorderColor: "#333",
          textBorderWidth: 2,
        },
      };

      var option = {
        color:[
          "#ff7437",
          "#5998e4",
          "#5D5EB4"
        ],
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          data: ["总人口", "感染人数", "感染人数变化"],
        },
        grid: {
          left: 20,
          right: 40,
          top: 15,
          bottom: 20,
        },
        xAxis: {
          type: "value",
          name: "人数",
          axisLabel: {
            formatter: "{value}",
            interval: 0,
          },
        },
        yAxis: {
          type: "category",
          inverse: true,
          data: this.cityname,
          axisLabel: {
            formatter: function (value) {
              return "{" + value + "| }\n{value|" + value + "}";
            },
            margin: 10,
            rich: {
              value: {
                lineHeight: 30,
                align: "center",
              },
            },
          },
        },
        series: [
          {
            name: "总人口",
            type: "bar",
            label: seriesLabel,
            data: this.citypeople,
          },
          {
            name: "感染人数",
            type: "bar",
            label: seriesLabel,
            data: this.cityInf,
          },
          {
            name: "感染人数变化",
            type: "bar",
            label: seriesLabel,
            data: this.cityNewInf,
          },
        ],
      };

      myChart.setOption(option);
    },

    DrawRoadMap() {
      // console.log("roadVol", this.roadVol);

      var myChart = echarts.init(document.getElementById("threebar"));

      // console.log("myChart", myChart);

      // console.log("cityname", this.cityname);

      // console.log("画个3D柱状图");

      var dataBJ = this.roadVol;

      var schema = [{ name: "date", index: 0, text: "日" }];

      var itemStyle = {
        opacity: 0.8,
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowOffsetY: 0,
        shadowColor: "rgba(0, 0, 0, 0.5)",
      };

      var option = {
        // backgroundColor: "#404a59",
        color: ["#dd4444", "#fec42c", "#80F1BE"],
        legend: {
          top: 10,
          data: ["北京"],
          textStyle: {
            color: "#fff",
            fontSize: 16,
          },
        },
        grid: {
          left: "10%",
          right: 150,
          top: "18%",
          bottom: "10%",
        },
        tooltip: {
          padding: 10,
          borderColor: "#777",
          borderWidth: 1,
          formatter: function (obj) {
            var value = obj.value;
            return (
              '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' +
              value[0] +
              "-" +
              value[1] +
              "：" +
              value[2]
            );
          },
        },
        xAxis: {
          type: "category",
          data: this.cityname,
          axisLabel: {
            color: "#777",
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: "#777",
            },
          },
          boundaryGap: false,
          splitLine: {
            show: true,
          },
        },
        yAxis: {
          type: "category",
          data: this.cityname,
          axisLabel: {
            color: "#777",
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: "#777",
            },
          },
          boundaryGap: false,
          splitLine: {
            show: true,
          },
        },
        visualMap: [
          {
            left: "right",
            bottom: "5%",
            dimension: 2,
            min: 0,
            max: 100,
            itemHeight: 120,

            precision: 0.1,
            text: ["明暗：人流量"],
            textGap: 30,
            textStyle: {
              color: "#000",
            },
            inRange: {
              colorLightness: [1, 0.5],
            },
            outOfRange: {
              color: ["rgba(255,255,255,.2)"],
            },
            controller: {
              inRange: {
                color: ["#c23531"],
              },
              outOfRange: {
                color: ["#444"],
              },
            },
          },
        ],
        series: [
          {
            type: "scatter",
            itemStyle: itemStyle,
            data: dataBJ,
          },
        ],
      };
      // console.log("快画完了");
      myChart.setOption(option);
      // console.log("画完了");
    },
  },
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";

body {
  overflow: hidden;
}

header {
  position: relative;
  height: 1.25rem;
  background: url("../../assets/img/head_bg3.png") no-repeat;
  height: 50px;
  width: 100%;
  background-size: 100% 100%;
}

h1 {
  font-style: 0.475rem;
  color: #fff;
  font-weight: bolder;
  text-align: center;
}

.layui-nav-tree .layui-nav-item a {
  font-weight: bold;
  background-color: rgb(131, 137, 158);
}

.layui-nav-tree .layui-nav-item a:hover {
  background-color: #55587e;
}

/* 第二三块的字体 */
.layui-nav-tree .layui-nav-child a {
  height: 40px;
  line-height: 40px;
  font-weight: normal;
  background-color: #fff;
  color: rgba(10, 12, 22, 0.411);
}

/* 第二三块的背景 */
.layui-nav-itemed > .layui-nav-child {
  display: block;
  padding: 0;
  background-color: rgba(212, 187, 187, 0.966);
}

/* 第二三块的hover */
.layui-nav .layui-nav-child a:hover {
  background-color: #55587e;
  color: rgb(255, 255, 255);
}

/* LOGO */
.layui-layout-admin .layui-logo {
  position: absolute;
  left: 0;
  top: 0;
  width: 200px;
  height: 50%;
  line-height: 40px;
  text-align: center;
  color: #ffffff;
}

.layui-layout-admin .layui-logotext {
  position: absolute;
  left: 0;
  top: 0;
  width: 200px;
  height: 50%;
  line-height: 80px;
  text-align: center;
  color: #ffffff;
}

.layui-layout-admin .layui-header {
  background-color: #8b9bbd;
}

.tools-wrapper {
  position: fixed;
  margin-top: 100px;
  width: 150px;
  height: 489px;
  background-color: #fff;
  border: 1px solid rgb(204, 204, 204);
  border-radius: 10px;
  box-shadow: 5px 5px 8px rgba(0, 0, 0, 0.1);
}

.tools-wrapper .el-button {
  display: block;
  width: 150px;
  height: 69px;
  color: grey;
  background-color: rgb(241, 245, 253);
  /* background-color: #bfa; */
  border: 1px solid transparent;
}

.tools-wrapper .el-button:hover {
  display: block;
  width: 150px;
  height: 69px;
  color: grey;
  background-image: linear-gradient(to right, rgb(93,96,181,0.5), rgb(89,151,227,0.5));
  /* background-color: #bfa; */
  border: 1px solid transparent;
}

.tools-wrapper button {
  display: block;
  width: 150px;
  height: 69px;
  color: #000;
  background-color: rgb(241, 245, 253);
  /* background-color: #bfa; */
  border: 1px solid transparent;
}

.tools-wrapper .stop-simulate button:hover {
  background-image: linear-gradient(to right, rgb(93,96,181,0.5), rgb(89,151,227,0.5));
}

.el-form-item {
  margin: 0;
}

.tools-wrapper .active1 {
  display: block;
  width: 150px;
  height: 69px;
  color: #000;
  border: 1px solid transparent;
  background-color: red;
  /* cursor: url(); */
}

.tools-wrapper .new-pointer {
  border-top: 1px solid transparent;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  /* box-shadow: 2px 2px rgba(0,0,0,.2); */
}

.tools-wrapper .new-pointer {
  border-top: 1px solid transparent;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  /* box-shadow: 2px 2px rgba(0,0,0,.2); */
}

.tools-wrapper .my-cases {
  height: 68px;
  border-bottom: 1px solid transparent;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.tools-wrapper .line {
  display: none;
  width: 150px;
  height: 1px;
  background-color: #999;
}

.tools-wrapper i {
  font-size: 22px;
}

.tools-wrapper span {
  margin-left: 5px;
  font-size: 20px;
}

.city-list {
  position: absolute;
  right: 0;
  width: 340px;
  height: 655px;
  padding-top: 20px;
  background-image: linear-gradient(to right, rgb(93,96,181,0.5), rgb(89,151,227,0.5));
  border-radius: 10px;
  box-shadow: -5px 5px 8px rgba(0, 0, 0, 0.1);
}

.city-list .title {
  display: block;
  font-size: 24px;
  margin-left: 5px;
  margin-bottom: 10px;
}

.city-list .panel {
  margin-left: 10px;
  width: 320px;
  height: 300px;
  border-radius: 10px;
  box-shadow: 2px 2px rgba(0, 0, 0, 0.2);
  background-color: #fff;
  /* border: 1px solid rgb(204, 204, 204); */
  border-radius: 10px;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}

.city-list div span {
  display: block;
  font-size: 16px;
  margin-left: 10px;
  margin-bottom: 3px;
}

.city-list .little-title {
  font-size: 20px;
  margin-top: 5px;
  margin-bottom: 10px;
}

h2 {
  height: 0.6rem;
  /* line-height: 0.6rem; */
  text-align: center;
  color: #000;
  font-size: 20px;
  font-weight: 400;
  margin-bottom: 15px;
}

.city-list #bar,
.city-list #threebar {
  top: 0;
  left: 0;
  width: 100%;
  height: 260px;
}

.add-wrapper {
  position: absolute;
  width: 70px;
  height: 100px;
  right: 240px;
}

.add-wrapper i {
  font-size: 70px;
  font-weight: bold;
}

.add-wrapper .add::after {
  display: none;
  content: "";
  position: absolute;
  width: 0;
  height: 0;
  border: 8px solid transparent;
  border-top: none;
  border-bottom-color: rgb(68, 68, 68);
  top: 69px;
  left: 28px;
  right: 0;
}

.add-wrapper button {
  display: none;
  height: 60px;
  width: 150px;
  margin-left: -80px;
  font-size: 15px;
  font-weight: normal;
  z-index: 999;
  background-color: rgb(68, 68, 68);
  border-bottom: 2px solid rgb(187, 187, 187);
}

.add-wrapper:hover button,
.add-wrapper:hover .add::after {
  display: block;
}

.add-wrapper button:hover {
  background-color: red;
}

.add-wrapper button:active {
  background-color: orange;
}

.add-wrapper button i {
  color: #fff;
  font-size: 18px;
  margin-left: -20px;
  margin-right: 5px;
}

.add-wrapper button span {
  color: #fff;
}

.add-wrapper .examples i {
  margin-left: -50px;
}

.add-wrapper .visualization i {
  margin-left: -10px;
}

.add-wrapper .cancellation i {
  margin-left: -48px;
}

.add-wrapper .cancellation {
  border-bottom: 2px solid transparent;
}

.layui-layout-right i {
  font-size: 24px;
}

.layui-layout-right .theme-wrapper {
  /* display: none; */
  position: absolute;
  height: 300px;
  width: 249px;
  background-color: #fff;
  border: 1px solid rgb(187, 187, 187);
  box-shadow: 2px 2px rgba(0, 0, 0, 0.2);
  margin-top: -5px;
  margin-left: 250px;
  z-index: 999;
  transition: margin-left 0.3s;
}

.layui-layout-right .theme:hover .theme-wrapper {
  margin-left: 0;
  display: block;
}

canvas {
  float: left;
}

.img-list {
  position: absolute;
  z-index: 6;
}

.img-list .city {
  display: none;
  position: absolute;
  /* left: 5000px;
  top: 3000px; */
}

.img-list .city .city-infor {
  position: absolute;
  display: block;
  height: 185px;
  width: 190px;
  margin-top: -240px;
  margin-left: 75px;
  border: 1px solid rgb(187, 187, 187);
  background-color: #ffffff;
  z-index: 9999;
}

.city-infor i{
  margin-right: 3px;
}

.img-list .city img {
  height: 100px;
  width: 100px;
}

.line_list .road_line {
  display: block;
  position: absolute;
  height: 10px;
  /* background-color: #000; */
  /* background: url(../../assets/img/road_line.png); */

  /* background: linear-gradient(to right, rgba(0, 0, 0, 0), #3446e6); */
  overflow: hidden;
}

.block {
  position: absolute;
  width: 800px;
  margin-left: 325px;
  margin-top: 600px;
}

.cityicon {
  margin-right: 8px;
}

.road_line span {
  position: absolute;
  display: block;
}

.road_line img {
  position: absolute;
  height: 10px;
  width: 750px;
  top: 0px;
  left: -100px;
  animation: roadmove1 3s linear infinite;
  z-index: 0;
}

.road_line span:nth-child(1) {
  height: 2px;
  width: 200px;
  top: 0px;
  left: -200px;
  background: linear-gradient(to right, rgba(0, 0, 0, 0), #f6e58d);
  border-top-right-radius: 1px;
  border-bottom-right-radius: 1px;
  animation: span1 2s linear infinite;
  animation-delay: 1s;
}

.road_line span:nth-child(2) {
  height: 2px;
  width: 200px;
  right: -200px;
  bottom: 0px;
  background: linear-gradient(to left, rgba(0, 0, 0, 0), #f6e58d);
  border-top-left-radius: 1px;
  border-bottom-left-radius: 1px;
  animation: span3 2s linear infinite;
  animation-delay: 3s;
}

@keyframes span1 {
  0% {
    left: -300px;
  }
  100% {
    left: 300px;
  }
}

@keyframes span3 {
  0% {
    right: -300px;
  }
  100% {
    right: 300px;
  }
}

@keyframes roadmove1 {
  0% {
    left: -100px;
  }
  100% {
    left: 0px;
  }
}
</style>

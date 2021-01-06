<template>
  <div id="settingMap">
    <header>
      <h1>地图模式</h1>
      <div class="toDIY">
        <button @click="toDIYModel">自定模式</button>
      </div>

      <div class="toMy">
        <router-link :to="{ path: '/Userprofile' }" style="margin-left: 10px; float: left"
          >个人中心</router-link
        >
      </div>
    </header>

    <section class="mainbox">
      <div class="column">
        <el-button type="primary" @click="add_city">增加城市</el-button>
        <el-button type="primary" @click="reduce_city">删除城市</el-button>
        <el-button type="primary" @click="save_case">保存案例</el-button>
        <div class="panel">
          <div>
            <span class="little-title">城市列表：</span>
            <li id="city_inf" v-for="city in city_po" :key="city">
              {{ city }}
            </li>
          </div>
          <div class="panel-footer"></div>
        </div>
      </div>

      <div class="column">
        <div class="map">
          <div class="map1"></div>
          <div class="map2"></div>
          <div class="map3"></div>
          <div class="chart" id="map"></div>
        </div>
      </div>

      <div class="column">
        <el-button type="primary" @click="add_road">增加双向航线</el-button>
        <el-button type="primary" @click="reduce_road">删除航线</el-button>
        <el-button type="primary" @click="begin_simulation">开始模拟</el-button>
        <div class="panel">
          <div>
            <span class="little-title">航线列表：</span>
            <li id="road_inf" v-for="road in road_di" :key="road">
              {{ road }}
            </li>
          </div>
          <div class="panel-footer"></div>
        </div>
      </div>
    </section>

    <el-dialog title="新增城市" :visible.sync="isShow1" :before-close="handleclose">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="druleForm"
      >
        <el-form-item>
          <label class="authority">选择城市： </label>
          <select id="selected" v-model="selected" name="authority">
            <option value="济南">济南</option>
            <option value="成都">成都</option>
            <option value="长沙">长沙</option>
            <option value="北京">北京</option>
            <option value="上海">上海</option>
            <option value="广州">广州</option>
            <option value="福州">福州</option>
            <option value="拉萨">拉萨</option>
            <option value="长春">长春</option>
            <option value="银川">银川</option>
            <option value="南京">南京</option>
            <option value="乌鲁木齐">乌鲁木齐</option>
            <option value="保定">保定</option>
            <option value="兰州">兰州</option>
            <option value="南宁">南宁</option>
            <option value="合肥">合肥</option>
            <option value="呼和浩特">呼和浩特</option>
            <option value="哈尔滨">哈尔滨</option>
            <option value="天津">天津</option>
            <option value="太原">太原</option>
            <option value="昆明">昆明</option>
            <option value="杭州">杭州</option>
            <option value="武汉">武汉</option>
            <option value="沈阳">沈阳</option>
            <option value="海口">海口</option>
            <option value="石家庄">石家庄</option>
            <option value="西安">西安</option>
            <option value="贵阳">贵阳</option>
            <option value="郑州">郑州</option>
            <option value="重庆">重庆</option>
            <option value="西宁">西宁</option>
          </select>
        </el-form-item>
        <el-form-item label="总人口" prop="to_pop" class="e_inp">
          <el-input v-model="ruleForm.to_pop"></el-input>
        </el-form-item>
        <el-form-item label="初始感染数" prop="begin_inf" class="e_inp">
          <el-input v-model="ruleForm.begin_inf"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="create_city">立即创建</el-button>
          <!-- <el-button type="info" @click="resetForm('ruleForm')">重置</el-button> -->
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="删除城市" :visible.sync="isShow3" :before-close="handleclose">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="druleForm"
      >
        <el-form-item>
          <label class="authority">选择城市： </label>
          <select id="selectedcity3" v-model="selected3" name="authority3">
            <option :value="types3.name" v-for="types3 in used_city1" :key="types3">
              {{ types3.name }}
            </option>
          </select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="delete_city">确认删除</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="新增航线" :visible.sync="isShow2" :before-close="handleclose">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="druleForm"
      >
        <el-form-item>
          <label class="authority">选择城市1： </label>
          <select id="selectedcity1" v-model="selected1" name="authority1">
            <option :value="types1.name" v-for="types1 in used_city1" :key="types1">
              {{ types1.name }}
            </option>
          </select>
        </el-form-item>

        <el-form-item>
          <label class="authority">选择城市2： </label>
          <select id="selectedcity2" v-model="selected2" name="authority2">
            <option :value="types2.name" v-for="types2 in used_city2" :key="types2">
              {{ types2.name }}
            </option>
          </select>
        </el-form-item>

        <el-form-item label="人流量" prop="volumn" class="vol">
          <el-input v-model="ruleForm.volumn"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="create_road">立即创建</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog title="删除航线" :visible.sync="isShow4" :before-close="handleclose">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="druleForm"
      >
        <el-form-item>
          <label class="authority">选择航线： </label>
          <select id="selectedcity4" v-model="selected4" name="authority4">
            <option :value="types4.name" v-for="types4 in used_road" :key="types4">
              {{ types4.name }}
            </option>
          </select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="delete_road">确认删除</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script src="http://g.tbcdn.cn/mtb/lib-flexible/0.3.4/??flexible_css.js,flexible.js"></script>

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
// import { flexible } from "../../assets/js/flexible.js";
import { jquery } from "../../assets/js/jquery.js";
var echarts = require("echarts");
import "../../../node_modules/echarts/lib/chart/map/china.js";

var citycnt = 0;
var roadcnt = 0;
var numReg = /^[0-9]*$/;
var numRe = new RegExp(numReg);

export default {
  data() {
    return {
      userId: 1,
      caseName: 0,

      city_po: [],
      road_di: [],

      used_city1: [],
      used_city2: [],
      used_road: [],
      selected1: "",
      selected2: "",
      selected3: "",
      selected4: "",

      road_data: [],

      isShow1: false,
      isShow2: false,
      isShow3: false,
      isShow4: false,

      ruleForm: {
        to_pop: "",
        begin_inf: "",
        volumn: "",
      },
      rules: {
        to_pop: [
          { required: true, message: "请输入总人口", trigger: "blur" },
          { min: 1, max: 6, message: "人口数量应在1到100000之间", trigger: "blur" },
        ],
        begin_inf: [
          { required: true, message: "请输入初始感染人数", trigger: "blur" },
          { min: 1, max: 4, message: "初始感染人数应该1到1000之间", trigger: "blur" },
        ],
        volumn: [
          { required: true, message: "请输入人流量", trigger: "blur" },
          { min: 1, max: 3, message: "人流量应该1到100之间", trigger: "blur" },
        ],
      },
    };
  },

  mounted: function () {
    console.log("地图模式初始化");

    this.GetUserIdentity();

    this.params = JSON.parse(this.$route.query.params);

    // console.log("用户ID：", this.params.userId);
    console.log("案例名：", this.params.caseName);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.InitCityData);
    console.log("道路信息：", this.params.InitRoadData);

    if (this.params.caseName != 999) {
      console.log("从地图模拟页面返回");

      citycnt = this.params.citynum;
      roadcnt = this.params.roadnum;

      var nowcnt = 0;
      var cn, totp, initinf;
      for (var i in this.params.InitCityData) {
        var te = this.params.InitCityData[i].split(":");
        var tte1 = te[1].split(",");
        var tte2 = te[2].split(",");
        cn = tte1[0];
        totp = tte2[0];
        initinf = te[3];
        var s = cn + ":总人口:" + totp + ",初始感染数:" + initinf;
        this.city_po.push(s);

        var newa = new Array();
        newa["id"] = nowcnt;
        newa["name"] = cn;
        this.used_city1.push(newa);
        this.used_city2.push(newa);
      }

      var cn1, cn2, vo;
      for (var i in this.params.InitRoadData) {
        var tr = this.params.InitRoadData[i].split(":");
        var ttr1 = tr[1].split(",");
        var ttr2 = tr[2].split(",");
        cn1 = ttr1[0];
        cn2 = ttr2[0];
        vo = tr[3];
        var s = cn1 + "-" + cn2 + ":" + vo;
        this.road_di.push(s);
      }
    } else {
      citycnt = 0;
      roadcnt = 0;
    }

    this.drawMap();
  },

  methods: {
    drawMap() {
      var myChart = echarts.init(document.getElementById("map"));
      var geoCoordMap = {
        上海: [121.4648, 31.2891],
        乌鲁木齐: [87.9236, 43.5883],
        保定: [115.0488, 39.0948],
        兰州: [103.5901, 36.3043],
        北京: [116.4551, 40.2539],
        南京: [118.8062, 31.9208],
        南宁: [108.479, 23.1152],
        合肥: [117.29, 32.0581],
        呼和浩特: [111.4124, 40.4901],
        哈尔滨: [127.9688, 45.368],
        天津: [117.4219, 39.4189],
        太原: [112.3352, 37.9413],
        广州: [113.5107, 23.2196],
        成都: [103.9526, 30.7617],
        拉萨: [91.1865, 30.1465],
        昆明: [102.9199, 25.4663],
        杭州: [119.5313, 29.8773],
        武汉: [114.3896, 30.6628],
        沈阳: [123.1238, 42.1216],
        济南: [117.1582, 36.8701],
        海口: [110.3893, 19.8516],
        石家庄: [114.4995, 38.1006],
        福州: [119.4543, 25.9222],
        西安: [109.1162, 34.2004],
        贵阳: [106.6992, 26.7682],
        郑州: [113.4668, 34.6234],
        重庆: [107.7539, 30.1904],
        银川: [106.3586, 38.1775],
        长春: [125.8154, 44.2584],
        长沙: [113.0823, 28.2568],
        西宁: [101.4038, 36.8207],
      };

      var XAData = [[{ name: "西安" }, { name: "西安", value: 0 }]];

      XAData = this.road_data;

      var planePath =
        "path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z";
      var convertData = function (data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
          var dataItem = data[i];

          var fromCoord = geoCoordMap[dataItem[0].name];
          var toCoord = geoCoordMap[dataItem[1].name];
          if (fromCoord && toCoord) {
            res.push({
              fromName: dataItem[0].name,
              toName: dataItem[1].name,
              coords: [fromCoord, toCoord],
              value: dataItem[1].value,
            });
          }
        }
        console.log("res:", res[1]);
        return res;
      };

      var color = ["#a6c84c", "#ffa022", "#46bee9"]; //航线的颜色
      var series = [];
      [
        ["西安", XAData],
        // ["西宁", XNData],
        // ["银川", YCData],
      ].forEach(function (item, i) {
        series.push(
          {
            name: item[0] + " Top3",
            type: "lines",
            zlevel: 1,
            effect: {
              show: true,
              period: 6,
              trailLength: 0.7,
              color: "red", //arrow箭头的颜色
              symbolSize: 3,
            },
            lineStyle: {
              normal: {
                color: color[i],
                width: 0,
                curveness: 0.2,
              },
            },
            data: convertData(item[1]),
          },
          {
            name: item[0] + " Top3",
            type: "lines",
            zlevel: 2,
            symbol: ["none", "arrow"],
            symbolSize: 10,
            effect: {
              show: true,
              period: 6,
              trailLength: 0,
              symbol: planePath,
              symbolSize: 15,
            },
            lineStyle: {
              normal: {
                color: color[i],
                width: 1,
                opacity: 0.6,
                curveness: 0.2,
              },
            },
            data: convertData(item[1]),
          },
          {
            name: item[0] + " Top3",
            type: "effectScatter",
            coordinateSystem: "geo",
            zlevel: 2,
            rippleEffect: {
              brushType: "stroke",
            },
            label: {
              normal: {
                show: true,
                position: "right",
                formatter: "{b}",
              },
            },
            symbolSize: function (val) {
              return val[2] / 8;
            },
            itemStyle: {
              normal: {
                color: color[i],
              },
              emphasis: {
                areaColor: "#2B91B7",
              },
            },
            data: item[1].map(function (dataItem) {
              return {
                name: dataItem[1].name,
                value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value]),
              };
            }),
          }
        );
      });
      var option = {
        tooltip: {
          trigger: "item",
          formatter: function (params, ticket, callback) {
            if (params.seriesType == "effectScatter") {
              return "线路：" + params.data.name + "" + params.data.value[2];
            } else if (params.seriesType == "lines") {
              return (
                params.data.fromName +
                ">" +
                params.data.toName +
                "<br />" +
                params.data.value
              );
            } else {
              return params.name;
            }
          },
        },
        legend: {
          orient: "vertical",
          top: "bottom",
          left: "right",
          data: ["西安 Top3", "西宁 Top3", "银川 Top3"],
          textStyle: {
            color: "#fff",
          },
          selectedMode: "multiple",
        },
        geo: {
          map: "china",
          label: {
            emphasis: {
              show: true,
              color: "#fff",
            },
          },
          // 把中国地图放大了1.2倍
          zoom: 1.2,
          roam: true,
          itemStyle: {
            normal: {
              // 地图省份的背景颜色
              areaColor: "rgba(20, 41, 87,0.6)",
              borderColor: "#195BB9",
              borderWidth: 1,
            },
            emphasis: {
              areaColor: "#2B91B7",
            },
          },
        },
        series: series,
      };
      myChart.setOption(option);
      // 监听浏览器缩放，图表对象调用缩放resize函数
      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },

    GetUserIdentity() {
      axios
        .post("/apis/backend/getIdentity/")
        .then((response) => {
          this.userId = response.data.userId;
          // alert(JSON.stringify(response.data)),
        })
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
    },

    add_city() {
      this.isShow1 = true;
    },

    create_city() {
      var cn = document.getElementById("selected").value;

      for (var i in this.city_po) {
        var tc = this.city_po[i].split(":");
        if (tc[0] == cn) {
          this.$alert("该城市已存在，请选择不同的城市", "创建失败", {
            confirmButtonText: "确定",
            callback: (action) => {
              this.$message({
                type: "info",
                message: "请重新创建",
              });
            },
          });
          this.isShow1 = false;
          return;
        }
      }

      if (!numRe.test(this.ruleForm.to_pop)) {
        this.isShow1 = false;
        this.$message({
          type: "error",
          message: "请输入数字",
        });
        this.ruleForm.to_pop = "";
        this.ruleForm.begin_inf = "";
        return;
      }

      if (!numRe.test(this.ruleForm.begin_inf)) {
        this.isShow1 = false;
        this.$message({
          type: "error",
          message: "请输入数字",
        });
        this.ruleForm.to_pop = "";
        this.ruleForm.begin_inf = "";
        return;
      }

      var ipp = parseInt(this.ruleForm.to_pop);
      if (ipp < 100 || ipp > 1000000) {
        this.$alert("城市人口应在100~1000000内", "创建失败", {
          confirmButtonText: "确定",
          callback: (action) => {
            this.$message({
              type: "info",
              message: "请重新创建",
            });
          },
        });
        this.isShow1 = false;
        return;
      }

      var ibi = parseInt(this.ruleForm.begin_inf);
      if (ibi < 1 || ibi > parseInt(ipp * 0.3)) {
        this.$alert("初始感染人数应至少为1人且不可多于总人口的30%", "创建失败", {
          confirmButtonText: "确定",
          callback: (action) => {
            this.$message({
              type: "info",
              message: "请重新创建",
            });
          },
        });
        this.isShow1 = false;
        return;
      }

      var s = cn + ":总人口:" + ipp + ",初始感染数:" + ibi;
      this.city_po.push(s);
      this.isShow1 = false;
      citycnt += 1;
      var newc = new Array();
      newc["id"] = citycnt;
      newc["name"] = cn;
      console.log("citycnt", citycnt);

      this.used_city1.push(newc);
      this.used_city2.push(newc);
      console.log("city1:", this.used_city1);
      console.log("city2:", this.used_city2);

      var newa = new Array();
      var c1 = {};
      var c2 = {};
      c1["name"] = cn;
      c2["name"] = cn;
      c2["value"] = 0;
      newa.push(c1);
      newa.push(c2);
      this.road_data.push(newa);

      this.drawMap();
    },

    reduce_city() {
      this.isShow3 = true;
    },

    delete_city() {
      var cn = document.getElementById("selectedcity3").value;
      for (var i in this.city_po) {
        var tc = this.city_po[i].split(":");
        if (tc[0] == cn) {
          this.city_po.splice(i, 1);
          break;
        }
      }

      // console.log("cn",cn);
      for (var i in this.used_city1) {
        // console.log("uc1i",this.used_city1[i]);
        if (this.used_city1[i]["name"] == cn) {
          console.log("可以删");
          this.used_city1.splice(i, 1);
          break;
        }
      }
      for (var i in this.used_city2) {
        if (this.used_city2[i]["name"] == cn) {
          this.used_city2.splice(i, 1);
          break;
        }
      }

      for (var i in this.road_di) {
        var tr = this.road_di[i].split(":");
        var ttr = tr[0].split("-");
        if (ttr[0] == cn || ttr[1] == cn) {
          this.road_di[i] = "";
        }
      }

      citycnt -= 1;

      this.isShow3 = false;

      // console.log("road_data",this.road_data);

      var wait_delete = [];

      for (var i in this.road_data) {
        if (this.road_data[i][0]["name"] == cn || this.road_data[i][1]["name"] == cn) {
          // this.road_data.splice(i,1);
          wait_delete.push(i);
        }
      }
      var twd = wait_delete.reverse();
      for (var i in twd) {
        this.road_data.splice(twd[i], 1);
      }

      // console.log("后road_data",this.road_data);
      this.drawMap();
    },

    add_road() {
      this.isShow2 = true;
    },

    create_road() {
      var cn1 = document.getElementById("selectedcity1").value;
      var cn2 = document.getElementById("selectedcity2").value;

      if (cn1 == cn2) {
        this.$alert("请选择两个不同的城市", "创建失败", {
          confirmButtonText: "确定",
          callback: (action) => {
            this.$message({
              type: "info",
              message: `action: ${action}`,
            });
          },
        });
        this.isShow2 = false;
        return;
      }

      for (var i in this.road_di) {
        var tc = this.road_di[i].split(":");
        var ttc = tc[0].split("-");
        if ((ttc[0] == cn1 && ttc[1] == cn2) || (ttc[1] == cn1 && ttc[0] == cn2)) {
          this.$alert("两城市间已存在航线，请选择不同的城市", "创建失败", {
            confirmButtonText: "确定",
            callback: (action) => {
              this.$message({
                type: "info",
                message: `action: ${action}`,
              });
            },
          });
          this.isShow2 = false;
          return;
        }
      }

      if (!numRe.test(this.ruleForm.volumn)) {
        this.$message({
          type: "error",
          message: "请输入数字",
        });
        this.ruleForm.volumn="";
        this.isShow2 = false;
        return;
      }

      var value = parseInt(this.ruleForm.volumn);
      if (value < 1 || value > 100) {
        this.$alert("人流量应在1~100内", "连接失败", {
          confirmButtonText: "确定",
          callback: (action) => {
            this.$message({
              type: "info",
              message: `action: ${action}`,
            });
          },
        });
        this.isShow2 = false;
        return;
      }

      var s = cn1 + "-" + cn2 + ":" + value;
      var rn = cn1 + "-" + cn2;
      console.log(s);
      this.road_di.push(s);
      console.log("se1:", this.selected1);
      console.log("se1:", this.selected2);

      roadcnt += 1;
      var newc = new Array();
      newc["id"] = roadcnt;
      newc["name"] = rn;

      this.used_road.push(newc);

      this.isShow2 = false;

      var newa = new Array();
      var newb = new Array();
      var c1 = {};
      var c2 = {};
      var c3 = {};
      var c4 = {};

      c1["name"] = cn1;
      c2["name"] = cn2;
      c2["value"] = value;
      newa.push(c1);
      newa.push(c2);
      this.road_data.push(newa);

      c3["name"] = cn2;
      c4["name"] = cn1;
      c4["value"] = value;
      newb.push(c3);
      newb.push(c4);
      this.road_data.push(newb);

      this.drawMap();
    },

    reduce_road() {
      this.isShow4 = true;
    },

    delete_road() {
      var rn = document.getElementById("selectedcity4").value;
      for (var i in this.road_di) {
        var tr = this.road_di[i].split(":");
        if (tr[0] == rn) {
          this.road_di.splice(i, 1);
          break;
        }
      }

      for (var i in this.used_road) {
        if (this.used_road[i]["name"] == rn) {
          this.used_road.splice(i, 1);
          break;
        }
      }

      roadcnt -= 1;

      this.isShow4 = false;

      var tr = rn.split("-");

      var wait_delete = [];

      console.log("前road_data", this.road_data);

      for (var i in this.road_data) {
        if (
          (this.road_data[i][0]["name"] == tr[0] &&
            this.road_data[i][1]["name"] == tr[1]) ||
          (this.road_data[i][0]["name"] == tr[1] && this.road_data[i][1]["name"] == tr[0])
        ) {
          // this.road_data.splice(i,1);
          wait_delete.push(i);
        }
      }
      var twd = wait_delete.reverse();
      for (var i in twd) {
        this.road_data.splice(twd[i], 1);
      }

      console.log("后road_data", this.road_data);
      this.drawMap();
    },

    save_case() {
      if (citycnt == 0) {
        this.$message({
          type: "warning",
          message: "您还未进行任何创建",
        });
        return;
      }

      this.$prompt("请输入此案例名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[\u4e00-\u9fa5_a-zA-Z0-9]{1,3}$/,
        inputErrorMessage: "案例名称可为汉字、英文字母和数字，长度为1到3个字符",
      })
        .then(({ value }) => {
          var myFormData = new FormData();

          myFormData.append("userId", this.userId);

          myFormData.append("caseName", value);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var loopcnt = 0;
          var citycnt = 0;
          console.log("城市信息", this.city_po);
          for (var cid in this.city_po) {
            citycnt += 1;
            var tc = this.city_po[cid].split(":");
            cn = tc[0];
            initinfect = tc[3];
            var ttc = tc[2].split(",");
            initpop = ttc[0];
            var s =
              "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
            city_infor.push(s);
            console.log("s", s);
          }
          myFormData.append("citynum", citycnt);

          var roadcnt = 0;
          var road_inf = [];
          var cn1, cn2, volume;
          for (var rid in this.road_di) {
            roadcnt += 1;
            var tr = this.road_di[rid].split("-");
            var ttr = tr[1].split(":");
            cn1 = tr[0];
            cn2 = ttr[0];
            volume = ttr[1];
            var s = "departure:" + cn1 + ",destination:" + cn2 + ",volume:" + volume;
            road_inf.push(s);
            console.log("rs", s);
          }
          myFormData.append("roadnum", roadcnt);
          myFormData.append("caseMode", 2);

          myFormData.append("InitCityData", city_infor);

          if (roadcnt == 0) {
            myFormData.append("InitRoadData", "NULL");
          } else {
            myFormData.append("InitRoadData", road_inf);
          }

          myFormData.append("CityPosition", "Empty");

          for (var value of myFormData.values()) {
            console.log(value);
          }

          axios
            .post("/apis/backend/saveCase/", myFormData)
            .then((response) => {
              // alert(JSON.stringify(response));
              this.$message({
                type: "success",
                message: "保存成功",
              });
            })
            .catch(function (error) {
              // alert(JSON.stringify(response));
              // alert("发送失败");
            });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    begin_simulation() {
      var myFormData = new FormData();

      myFormData.append("userId", this.userId);

      myFormData.append("caseName", 99);

      var city_infor = [];
      var cn = "Z";
      var initpop = 0;
      var initinfect = 0;
      var loopcnt = 0;
      var citycnt = 0;
      console.log("城市信息", this.city_po);
      for (var cid in this.city_po) {
        citycnt += 1;
        var tc = this.city_po[cid].split(":");
        cn = tc[0];
        initinfect = tc[3];
        var ttc = tc[2].split(",");
        initpop = ttc[0];
        var s = "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
        city_infor.push(s);
        console.log("s", s);
      }
      myFormData.append("citynum", citycnt);

      console.log("citycnt", citycnt);

      if (citycnt == 0) {
        this.$message({
          type: "warning",
          message: "您还未进行任何创建",
        });
        return;
      }

      var roadcnt = 0;
      var road_inf = [];
      var cn1, cn2, volume;
      for (var rid in this.road_di) {
        roadcnt += 1;
        var tr = this.road_di[rid].split("-");
        var ttr = tr[1].split(":");
        cn1 = tr[0];
        cn2 = ttr[0];
        volume = ttr[1];
        var s = "departure:" + cn1 + ",destination:" + cn2 + ",volume:" + volume;
        road_inf.push(s);
        console.log("rs", s);
      }
      myFormData.append("roadnum", roadcnt);
      myFormData.append("caseMode", 2);

      myFormData.append("InitCityData", city_infor);

      if (roadcnt == 0) {
        myFormData.append("InitRoadData", "NULL");
      } else {
        myFormData.append("InitRoadData", road_inf);
      }

      myFormData.append("CityPosition", "Empty");

      myFormData.append("daynum", 365);

      for (var value of myFormData.values()) {
        console.log(value);
      }

      axios
        .post("/apis/backend/startSimulate/", myFormData)
        .then((response) => {
          // alert(JSON.stringify(response));
          alert("开始模拟");

          this.$router.push({
            path: "/simulationMap",
            query: {
              params: JSON.stringify({
                caseName: 99,
                citynum: citycnt,
                roadnum: roadcnt,
                InitCityData: city_infor,
                InitRoadData: road_inf,
                Daynum: 365,
                DailyInfected: response,
              }),
            },
          });
        })
        .catch(function (error) {
          // alert(JSON.stringify(response));
          // alert("发送失败");
        });
    },

    handleclose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },

    toDIYModel() {
      this.$router.push({
        path: "/setting",
        query: {
          params: JSON.stringify({
            userId: this.userId,
            caseName: 999,
          }),
        },
      });
    },
  },
};
</script>

<style scoped>
/* @import "../../assets/layui/css/layui.css"; */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

li {
  list-style: none;
}

#simulationMap {
  /* background: url("../../assets/img/bg.jpg") no-repeat top center; */
  line-height: 1.15;
  height: 655px;
  width: 100%;
  background-size: 100% 100%;
}

header {
  position: relative;
  height: 1.25rem;
  background: url("../../assets/img/head_bg.png") no-repeat;
  height: 50px;
  width: 100%;
  background-size: 100% 100%;
}

h1 {
  font-style: 0.475rem;
  color: #fff;
  text-align: center;
}

header .toDIY {
  position: absolute;
  left: 5px;
  top: 5px;
}

.toDIY button {
  /* background-color: rgb(149, 154, 169); */
  background-color: transparent;
  color: white;
  font-size: 20px;
  border: none;
}

header .toMy {
  position: absolute;
  right: 5px;
  top: 5px;
}

.toMy a {
  font-size: 20px;
  color: white;
  text-decoration: none;
}

.mainbox {
  display: flex;
  min-width: 1024px;
  max-width: 1920px;
  margin: 0 auto;
  padding: 10px 10px 0;
}

.mainbox .column {
  flex: 3;
}

.mainbox .column:nth-child(2) {
  margin: 0 10px 15px 0;
}

.mainbox .column:nth-child(2) {
  flex: 5;
}

.mainbox .column .panel {
  position: relative;
  height: 600px;
  padding: 0 15px 40px;
  margin-bottom: 15px;
  border: 1px solid rgba(25, 186, 139, 0.17);
  background: url("../../assets/img/line.png") rgba(255, 255, 255, 0.04);
}

.mainbox .column .panel::before {
  position: absolute;
  top: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: "";
}

.mainbox .column .panel::after {
  position: absolute;
  top: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-top: 2px solid #02a6b5;
  content: "";
}

.mainbox .column .panel .panel-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
}

.mainbox .column .panel .panel-footer::before {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 10px;
  height: 10px;
  border-left: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: "";
}

.mainbox .column .panel .panel-footer::after {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 10px;
  height: 10px;
  border-right: 2px solid #02a6b5;
  border-bottom: 2px solid #02a6b5;
  content: "";
}

.map {
  position: relative;
  height: 630px;
}

.map .map1 {
  width: 310px;
  height: 310px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: url("../../assets/img/map.png");
  background-size: 100% 100%;
  opacity: 0.3;
}

.map .map2 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 370px;
  height: 370px;
  background: url("../../assets/img/lbx.png");
  background-size: 100% 100%;
  animation: rotate1 15s linear infinite;
  opacity: 0.6;
}

.map .map3 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 335px;
  height: 335px;
  background: url("../../assets/img/jt.png");
  background-size: 100% 100%;
  animation: rotate2 15s linear infinite;
  opacity: 0.6;
}

.map .chart {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 500px;
}

.mainbox .column .el-button--primary {
  height: 30px;
  width: 110px;
  margin-bottom: 10px;
}

.druleForm .el-button--primary,
.druleForm .el-button--info {
  height: 30px;
  width: 100px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.druleForm .el-input {
  margin-bottom: 10px;
}

.authority {
  position: absolute;
  margin-left: -75px;
}

@keyframes rotate1 {
  form {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

@keyframes rotate2 {
  form {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  to {
    transform: translate(-50%, -50%) rotate(-360deg);
  }
}
</style>

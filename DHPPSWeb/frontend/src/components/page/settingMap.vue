<template>
  <div id="settingMap">
    <header>
      <h1>地图模式</h1>
    </header>

    <section class="mainbox">
      <div class="column">
        <el-button type="primary" @click="add_city">增加城市</el-button>
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
        <el-button type="primary" @click="save_case">保存案例</el-button>
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
        <!-- <el-form-item label="问题" prop="question">
          <el-input v-model="ruleForm.question"></el-input>
        </el-form-item> -->
        <el-form-item>
          <label class="authority">选择城市： </label>
          <select id="selected" v-model="selected" name="authority">
            <option value="济南">济南</option>
            <option value="成都">成都</option>
            <option value="长沙">长沙</option>
            <option value="北京">北京</option>
            <option value="上海">上海</option>
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

    <el-dialog title="新增航线" :visible.sync="isShow2" :before-close="handleclose">
      <el-form
        :model="ruleForm"
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="druleForm"
      >
        <!-- <el-form-item label="问题" prop="question">
          <el-input v-model="ruleForm.question"></el-input>
        </el-form-item> -->
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
  </div>
</template>

<script>
import { flexible } from "../../assets/js/flexible.js";
import { jquery } from "../../assets/js/jquery.js";
var echarts = require("echarts");
import "../../../node_modules/echarts/lib/chart/map/china.js";

var citycnt = 0;

export default {
  data() {
    return {
      userId: 1,

      city_po: [],
      road_di: [],

      used_city1: [
        // { id: 1, name: "济南" },
        // { id: 2, name: "成都" },
      ],
      used_city2: [],
      selected1: "",
      selected2: "",

      isShow1: false,
      isShow2: false,
      ruleForm: {
        to_pop: "",
        begin_inf: "",
        volumn: "",
      },
      rules: {
        to_pop: [
          { required: true, message: "请输入总人口", trigger: "blur" },
          { min: 3, max: 150, message: "长度在 3 到 150 个字符", trigger: "blur" },
        ],
        begin_inf: [
          { required: true, message: "请输入初始感染人数", trigger: "blur" },
          { min: 3, max: 150, message: "长度在 3 到 150 个字符", trigger: "blur" },
        ],
        volumn: [
          { required: true, message: "请输入人流量", trigger: "blur" },
          { min: 3, max: 150, message: "长度在 3 到 150 个字符", trigger: "blur" },
        ],
      },
    };
  },
  mounted: function () {
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

      var XNData = [];

      var YCData = [];

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

    add_city() {
      this.isShow1 = true;
    },

    create_city() {
      var cn = document.getElementById("selected").value;
      var s =
        cn +
        ": 总人口:" +
        this.ruleForm.to_pop +
        ",初始感染数:" +
        this.ruleForm.begin_inf;
      this.city_po.push(s);
      this.isShow1 = false;
      // this.used_city1[citycnt]["id"]=citycnt+1;
      // this.used_city1[citycnt]["name"]=cn;
      // this.used_city2[citycnt]["id"]=citycnt+1;
      // this.used_city2[citycnt]["name"]=cn;
      citycnt += 1;
      // this.used_city1['id']=1;
      // this.used_city1['name']="济南";
      var newc = new Array();
      newc["id"] = citycnt;
      newc["name"] = cn;

      this.used_city1.push(newc);
      this.used_city2.push(newc);
      console.log("city1:", this.used_city1);

      // newc['id']=3;
      // newc['name']="上海";
      // console.log("new:",newc);

      // this.used_city1.push(newc);
      // console.log("city1:",this.used_city1);
      console.log("city2:", this.used_city2);
    },

    add_road() {
      this.isShow2 = true;
    },

    create_road() {
      var cn1 = document.getElementById("selectedcity1").value;
      var cn2 = document.getElementById("selectedcity2").value;
      var s = cn1 + "-" + cn2 + ":" + this.ruleForm.volumn;
      console.log(s);
      this.road_di.push(s);
      console.log("se1:", this.selected1);
      console.log("se1:", this.selected2);
      this.isShow2 = false;
    },

    save_case() {
      this.$prompt("请输入此案例名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "案例名称格式不正确",
      })
        .then(({ value }) => {
          this.sc = false;

          var myFormData = new FormData();

          myFormData.append("userid", this.userId);

          myFormData.append("casename", value);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var citycnt = 0;

          for (var cid in this.city_po) {
            var te1 = this.city_po[cid].split(":");
            var te2 = te1[2].split(",");
            cn = te1[0];
            initpop = te2[0];
            initinfect = te1[3];
            citycnt += 1;
            var s =
              "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
            city_infor.push(s);
          }
          myFormData.append("citynum", citycnt);

          var roadcnt = 0;
          var road_inf = [];
          for (var rid in this.road_di) {
            var te1 = this.road_di[rid].split(":");
            var te2 = te1[0].split("-");
            roadcnt += 1;
            var departure = te2[0];
            var destination = te2[1];
            var volume = te1[1];
            var s =
              "departure:" +
              departure +
              ",destination:" +
              destination +
              ",volume:" +
              volume;
            road_inf.push(s);
          }
          myFormData.append("roadnum", roadcnt);

          myFormData.append("Initcitydata", city_infor);
          myFormData.append("Initroaddata", road_inf);

          for (var value of myFormData.values()) {
            console.log(value);
          }

          axios
            .post("http://127.0.0.1:8000/backend/saveCase/", myFormData)
            .then((response) => {
              // alert(JSON.stringify(response));
              // alert("保存案例");
            })
            .catch(function (error) {
              // alert(JSON.stringify(response));
              // alert("发送失败");
            });
        })
        .catch(() => {
          this.sc = false;
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    begin_simulation() {
      var myFormData = new FormData();

      myFormData.append("userid", this.userId);

      myFormData.append("casename", 99);

      var city_infor = [];
      var cn = "Z";
      var initpop = 0;
      var initinfect = 0;
      var citycnt = 0;

      for (var cid in this.city_po) {
        var te1 = this.city_po[cid].split(":");
        var te2 = te1[2].split(",");
        cn = te1[0];
        initpop = te2[0];
        initinfect = te1[3];
        citycnt += 1;
        var s = "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
        city_infor.push(s);
      }
      myFormData.append("citynum", citycnt);

      var roadcnt = 0;
      var road_inf = [];
      for (var rid in this.road_di) {
        var te1 = this.road_di[rid].split(":");
        var te2 = te1[0].split("-");
        roadcnt += 1;
        var departure = te2[0];
        var destination = te2[1];
        var volume = te1[1];
        var s =
          "departure:" + departure + ",destination:" + destination + ",volume:" + volume;
        road_inf.push(s);
      }
      myFormData.append("roadnum", roadcnt);

      myFormData.append("Initcitydata", city_infor);
      myFormData.append("Initroaddata", road_inf);

      for (var value of myFormData.values()) {
        console.log(value);
      }

      axios
        .post("http://127.0.0.1:8000/backend/startSimulate/", myFormData)
        .then((response) => {
          // alert(JSON.stringify(response));
          // alert("开始模拟");
          this.$router.push({
            path: "/simulation",
            query: {
              params: JSON.stringify({
                userid: this.userId,
                casename: 99,
                citynum: citycnt,
                roadnum: roadcnt,
                Initcitydata: city_infor,
                Initroaddata: road_inf,
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
  height: 540px;
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
  height: 570px;
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
  /* animation: rotate1 15s linear infinite; */
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
  /* animation: rotate2 15s linear infinite; */
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

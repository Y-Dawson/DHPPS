<template>
  <div id="simulationMap">
    <header>
      <h1>数据可视化</h1>
      <div class="stop">
        <button @click="stopSimulation">停止模拟</button>
      </div>
    </header>

    <section class="mainbox">
      <div class="column">
        <div class="no">
          <div class="no-hd">
            <ul>
              <li>{{ total_people }}</li>
              <li>{{ highest_infected }}</li>
            </ul>
          </div>

          <div class="no-bd">
            <ul>
              <li>总人口</li>
              <li>感染人数峰值</li>
            </ul>
          </div>
        </div>

        <div class="map">
          <div class="map1"></div>
          <div class="map2"></div>
          <div class="map3"></div>
          <div class="chart" id="map"></div>
        </div>
      </div>

      <div class="column">
        <div class="panel">
          <h2>各城市感染人数折线图</h2>
          <div class="chart" id="line"></div>
          <div class="panel-footer"></div>
        </div>

        <div class="panel">
          <h2>感染人数峰值各城市占比图</h2>
          <div class="chart" id="pie"></div>
          <div class="panel-footer"></div>
        </div>
      </div>
    </section>
  </div>
</template>
<script src="http://g.tbcdn.cn/mtb/lib-flexible/0.3.4/??flexible_css.js,flexible.js"></script>
<script>
// import { echarts } from "../../assets/js/echarts.min.js";

// import { flexible } from "../../assets/js/flexible.js";
import { jquery } from "../../assets/js/jquery.js";
// import { china } from "../../assets/js/china.js";

var echarts = require("echarts");
import "../../../node_modules/echarts/lib/chart/map/china.js";
// var china = require("../../assets/js/china.js");
// import { china } from "../../assets/js/china.js";

export default {
  data() {
    return {
      total_people: 0,
      highest_infected: 0,

      citynamelist: [],
      linemap_information: [],
      piemap_information: [],
      map_information: [],

      userId: 0,
      caseName: 0,
      citynum: 0,
      roadnum: 0,
      city_inf: [],
      road_inf: [],
    };
  },
  mounted: function () {
    this.GetUserIdentity();

    this.params = JSON.parse(this.$route.query.params);

    // console.log("用户ID：", this.params.userId);
    console.log("案例名：", this.params.caseName);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.InitCityData);
    console.log("道路信息：", this.params.InitRoadData);
    console.log("每日病例：", this.params.DailyInfected.data.DailyForecastData);
    var foreData = this.params.DailyInfected.data.DailyForecastData;

    // this.userId = this.params.userId;
    this.caseName = this.params.caseName;
    this.citynum = this.params.citynum;
    this.roadnum = this.params.roadnum;
    this.city_inf = this.params.InitCityData;
    this.road_inf = this.params.InitRoadData;

    for (var j = 0; j < parseInt(this.params.citynum); j++) {
      this.total_people += parseInt(foreData[364][j]["population"]);
      // this.highest_infected += parseInt(foreData[364][j]["infected"]);
    }

    var maxInf = 0;
    var d = -1;
    for (var i = 0; i < 365; i++) {
      var temp = 0;
      for (var j = 0; j < parseInt(this.params.citynum); j++) {
        temp += parseInt(foreData[i][j]["infected"]);
      }
      if (temp > maxInf) {
        maxInf = temp;
        d = i;
      }
    }
    this.highest_infected = maxInf;

    var cn;
    for (var j in this.params.InitCityData) {
      console.log(this.params.InitCityData[j]);
      var tc = this.params.InitCityData[j].split(":");
      var ttc = tc[1].split(",");
      cn = ttc[0];
      this.citynamelist.push(cn);
    }

    console.log("citynamelist", this.citynamelist);

    for (var j in this.citynamelist) {
      var newa = {};
      newa["name"] = this.citynamelist[j];
      newa["type"] = "line";
      var newb = new Array();

      newb.push(foreData[0][j]["infected"]);
      newb.push(foreData[14][j]["infected"]);
      newb.push(foreData[28][j]["infected"]);
      newb.push(foreData[42][j]["infected"]);
      newb.push(foreData[56][j]["infected"]);
      newb.push(foreData[70][j]["infected"]);
      newb.push(foreData[84][j]["infected"]);
      newb.push(foreData[98][j]["infected"]);
      newb.push(foreData[112][j]["infected"]);
      newb.push(foreData[126][j]["infected"]);
      newb.push(foreData[140][j]["infected"]);
      newb.push(foreData[154][j]["infected"]);
      newa["data"] = newb;

      newa["smooth"] = "true";

      this.linemap_information.push(newa);
    }

    console.log("series", this.linemap_information);

    for (var j in this.citynamelist) {
      var newc = {};
      newc["value"] = foreData[d][j]["infected"];
      newc["name"] = this.citynamelist[j];
      this.piemap_information.push(newc);
    }

    console.log("pieinf", this.piemap_information);

    console.log("road_inf", this.params.InitRoadData);

    var road_data = [];
    for (var j in this.params.InitRoadData) {
      var newa = new Array();
      var c1 = {};
      var c2 = {};
      var te = this.params.InitRoadData[j].split(":");
      var tte1 = te[1].split(",");
      var tte2 = te[2].split(",");
      console.log("te", te);
      c1["name"] = tte1[0];
      c2["name"] = tte2[0];
      c2["value"] = parseInt(te[3]);
      newa.push(c1);
      newa.push(c2);
      console.log("newa", newa);
      road_data.push(newa);
    }

    console.log("road_data", road_data);
    // this.map_information.push(road_data);
    this.map_information = road_data;
    console.log("mapinf", this.map_information);

    var YCData = [
      [{ name: "拉萨" }, { name: "济南", value: 100 }],
      [{ name: "拉萨" }, { name: "哈尔滨", value: 100 }],
      [{ name: "银川" }, { name: "上海", value: 100 }],
      [{ name: "银川" }, { name: "西安", value: 100 }],
      [{ name: "银川" }, { name: "西宁", value: 100 }],
    ];

    console.log("ycdata", YCData);

    this.drawLine();

    this.drawPie();

    this.drawMap(this.params.InitRoadData);
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
              path: "/Login",
            });
          }
          // alert(JSON.stringify(response.data)),
        })
        .catch(function (error) {
          // alert(JSON.stringify(error.response.data.message));
          alert("获取用户身份失败");
        });
    },

    drawLine() {
      var myChart = echarts.init(document.getElementById("line"));
      var option = {
        color: [
          "#00f2f1",
          "#ed3f35",
          "#1089E7",
          "#F57474",
          "#56D0E3",
          "#F8B448",
          "#8B78F6",
        ],
        tooltip: {
          trigger: "axis",
        },
        legend: {
          textStyle: {
            color: "#4c9bfd",
          },
          right: "10%",
          data: this.citynamelist,
        },
        grid: {
          top: "20%",
          left: "3%",
          right: "4%",
          bottom: "3%",
          show: true,
          borderColor: "#012f4a",
          containLabel: true,
        },
        // toolbox: {
        //   feature: {
        //     saveAsImage: {},
        //   },
        // },
        xAxis: {
          type: "category",
          data: [
            "1.01",
            "1.15",
            "1.29",
            "2.12",
            "2.26",
            "3.12",
            "3.26",
            "4.09",
            "4.23",
            "5.07",
            "5.21",
            "6.04",
          ],
          axisTick: {
            show: false,
          },
          axisLabel: {
            color: "#4c9bfd",
          },
          axisLine: {
            show: false,
          },
          boundaryGap: false,
        },
        yAxis: {
          type: "value",
          axisTick: {
            show: false,
          },
          axisLabel: {
            color: "#4c9bfd",
          },
          axisLine: {
            show: false,
          },
          boundaryGap: false,
          splitLine: {
            lineStyle: {
              color: "#012f4a",
            },
          },
        },
        series: this.linemap_information,
      };
      myChart.setOption(option);

      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },

    drawPie() {
      var myChart = echarts.init(document.getElementById("pie"));
      var option = {
        color: [
          "#006cff",
          "#60cda0",
          "#ed8884",
          "#ff9f7f",
          "#0096ff",
          "#9fe6b8",
          "#32c5e9",
          "#1d9dff",
        ],
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)",
        },
        // legend: {
        //   textStyle: {
        //     color: "rgba(255,255,255,.5)",
        //     fontSize: "12",
        //   },
        //   left: "center",
        //   bottom: "0%",
        //   itemWidth: 10,
        //   itemHeight: 10,
        //   data: this.citynamelist,
        // },
        series: [
          {
            name: "地区分布",
            type: "pie",
            radius: ["10%", "70%"],
            center: ["50%", "50%"],
            roseType: "radius",
            label: {
              fontSize: 12,
            },
            labelLine: {
              length: 10,
            },
            data: this.piemap_information,
          },
        ],
      };
      myChart.setOption(option);

      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },

    drawMap(mapData) {
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

      var road_data = [];
      for (var j in mapData) {
        var newa = new Array();
        var newb = new Array();
        var c1 = {};
        var c2 = {};
        var c3 = {};
        var c4 = {};

        var te = this.params.InitRoadData[j].split(":");
        var tte1 = te[1].split(",");
        var tte2 = te[2].split(",");
        console.log("te", te);
        c1["name"] = tte1[0];
        c2["name"] = tte2[0];
        c2["value"] = parseInt(te[3]);
        newa.push(c1);
        newa.push(c2);
        console.log("newa", newa);
        road_data.push(newa);

        c3["name"] = tte2[0];
        c4["name"] = tte1[0];
        c4["value"] = parseInt(te[3]);
        newb.push(c3);
        newb.push(c4);
        console.log("newb", newb);
        road_data.push(newb);
      }

      for (var j in this.citynamelist) {
        var newa = new Array();
        var c1 = {};
        var c2 = {};
        c1["name"] = this.citynamelist[j];
        c2["name"] = this.citynamelist[j];
        c2["value"] = 0;
        newa.push(c1);
        newa.push(c2);
        road_data.push(newa);
      }

      var XAData = road_data;
      console.log("mapData", mapData);
      console.log("XAData", XAData);

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
        // console.log("res[1]:", res[1]);
        return res;
      };

      var color = ["#a6c84c", "#ffa022", "#46bee9"]; //航线的颜色
      var series = [];
      [["西安", XAData]].forEach(function (item, i) {
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
              return val[2] / 80;
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
          data: ["西安 Top1", "西宁 Top2", "银川 Top2"],
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

    stopSimulation() {
      this.$router.push({
        path: "/settingMap",
        query: {
          params: JSON.stringify({
            caseName: this.caseName,
            citynum: this.citynum,
            roadnum: this.roadnum,
            InitCityData: this.city_inf,
            InitRoadData: this.road_inf,
          }),
        },
      });
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

li {
  list-style: none;
}

body {
  overflow: hidden;
}
/* @font-face {
    font-family: 'electronicFont';
    src: url('../../assets/layui/font/DS-DIGIT.TTF');
} */

#simulationMap {
  /* background: url(../../assets/img/bg.jpg) no-repeat top center; */
  line-height: 1.15;
  height: 720px;
  width: 100%;
  background-size: 100% 100%;
}

header {
  position: relative;
  height: 1.25rem;
  background: url(../../assets/img/head_bg2.png) no-repeat;
  height: 50px;
  width: 100%;
  background-size: 100% 100%;
}

h1 {
  font-style: 0.475rem;
  color: #fff;
  text-align: center;
}

h2 {
  height: 0.6rem;
  /* line-height: 0.6rem; */
  text-align: center;
  color: #000;
  font-size: 20px;
  font-weight: 400;
  margin-top: 10px;
  margin-bottom: 10px;
}

header .stop {
  position: absolute;
  right: 5px;
  top: 5px;
}

.stop button {
  background-color: transparent;
  color: white;
  font-size: 20px;
  border: none;
}

.mainbox {
  display: flex;
  min-width: 1024px;
  max-width: 1920px;
  margin: 0 auto;
  padding: 10px 10px 0;
}

.mainbox .column {
  flex: 4;
}

.mainbox .column:nth-child(1) {
  margin: 0 10px 15px 0;
}

.mainbox .column .panel {
  position: relative;
  height: 310px;
  padding: 0 15px 40px;
  margin-bottom: 15px;
  border: 1px solid rgba(25, 186, 139, 0.17);
  background: url(../../assets/img/line.png) rgba(255, 255, 255, 0.04);
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

.mainbox .column .panel .chart {
  width: 100%;
  height: 230px;
}

.mainbox .column .panel #pie {
  width: 100%;
  height: 230px;
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

.no {
  background: rgba(101, 132, 226, 0.1);
  padding: 15px;
}

.no .no-hd {
  position: relative;
  border: 1px solid rgba(25, 186, 139, 0.17);
}

.no .no-hd ul {
  display: flex;
}

.no .no-hd ul li {
  position: relative;
  flex: 1;
  line-height: 50px;
  font-size: 40px;
  color: #ff9f7f;
  text-align: center;
  /* font-family: "electronicFont"; */
}

.no .no-hd ul li:nth-child(1)::after {
  position: absolute;
  content: "";
  top: 25%;
  height: 50%;
  width: 1px;
  right: 0;
  background: rgba(255, 255, 255, 0.2);
}

.no .no-hd::before {
  position: absolute;
  top: 0;
  left: 0;
  content: "";
  width: 30px;
  height: 10px;
  border-top: 2px solid #02a6b5;
  border-left: 2px solid #02a6b5;
}

.no .no-hd::after {
  position: absolute;
  bottom: 0;
  right: 0;
  content: "";
  width: 30px;
  height: 10px;
  border-bottom: 2px solid #02a6b5;
  border-right: 2px solid #02a6b5;
}

.no .no-bd ul {
  display: flex;
}

.no .no-bd ul li {
  flex: 1;
  text-align: center;
  color: #000;
  font-size: 18px;
  height: 12px;
  padding-top: 2px;
}

.map {
  position: relative;
  height: 480px;
}

.map .map1 {
  width: 310px;
  height: 310px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: url(../../assets/img/map.png);
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
  background: url(../../assets/img/lbx.png);
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
  background: url(../../assets/img/jt.png);
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

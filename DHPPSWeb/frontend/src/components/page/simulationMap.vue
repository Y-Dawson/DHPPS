<template>
  <div id="simulationMap">
    <header>
      <h1>数据可视化</h1>
    </header>

    <section class="mainbox">
      <div class="column">
        <div class="no">
          <div class="no-hd">
            <ul>
              <li>{{ total_people }}</li>
              <li>{{ total_infected }}</li>
            </ul>
          </div>

          <div class="no-bd">
            <ul>
              <li>总人口</li>
              <li>总感染人数</li>
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
          <h2>折线图</h2>
          <div class="chart" id="line"></div>
          <div class="panel-footer"></div>
        </div>

        <div class="panel">
          <h2>饼形图</h2>
          <div class="chart" id="pie"></div>
          <div class="panel-footer"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
// import { echarts } from "../../assets/js/echarts.min.js";

import { flexible } from "../../assets/js/flexible.js";
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
      total_infected: 0,

      citynamelist: [],
      linemap_information: [],
    };
  },
  mounted: function () {
    this.params = JSON.parse(this.$route.query.params);

    console.log("用户ID：", this.params.userId);
    console.log("案例名：", this.params.caseName);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.InitCityData);
    console.log("道路信息：", this.params.InitRoadData);
    console.log("每日病例：", this.params.DailyInfected.data.DailyForecastData);
    var foreData = this.params.DailyInfected.data.DailyForecastData;

    for (var j = 0; j < parseInt(this.params.citynum); j++) {
      this.total_people += parseInt(foreData[364][j]["population"]);
      this.total_infected += parseInt(foreData[364][j]["infected"]);
    }

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
      var newa = new Array();
      newa["name"] = this.citynamelist[j];
      newa["type"] = "line";
      var newb = new Array();

      newb.push(foreData[0][j]["infected"]);
      newb.push(foreData[31][j]["infected"]);
      newb.push(foreData[59][j]["infected"]);
      newb.push(foreData[90][j]["infected"]);
      newb.push(foreData[120][j]["infected"]);
      newb.push(foreData[151][j]["infected"]);
      newb.push(foreData[181][j]["infected"]);
      newb.push(foreData[212][j]["infected"]);
      newb.push(foreData[243][j]["infected"]);
      newb.push(foreData[273][j]["infected"]);
      newb.push(foreData[304][j]["infected"]);
      newb.push(foreData[334][j]["infected"]);
      newa["data"] = newb;

      newa["smooth"] = "true";

      console.log("newa",newa);

      this.linemap_information.push(newa);
    }

    alert(this.linemap_information);
    console.log("series",this.linemap_information);

    this.drawLine();

    this.drawPie();

    this.drawMap();
  },
  methods: {
    drawLine() {
      var myChart = echarts.init(document.getElementById("line"));
      var option = {
        color: ["#00f2f1", "#ed3f35"],
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
            "一月",
            "二月",
            "三月",
            "四月",
            "五月",
            "六月",
            "七月",
            "八月",
            "九月",
            "十月",
            "十一月",
            "十二月",
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
        // [
        //   {
        //     name: "济南",
        //     type: "line",
        //     data: [120, 132, 101, 134, 90, 230, 210, 120, 130, 150, 180, 220],
        //     smooth: true,
        //   },
        //   {
        //     name: "成都",
        //     type: "line",
        //     data: [220, 182, 191, 234, 290, 330, 310, 330, 240, 260, 280, 500],
        //     smooth: true,
        //   },
        // ],
      };
      myChart.setOption(option);
      // myChart.setOption({
      //   series: this.linemap_information
      // });

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
        legend: {
          textStyle: {
            color: "rgba(255,255,255,.5)",
            fontSize: "12",
          },
          left: "center",
          bottom: "0%",
          itemWidth: 10,
          itemHeight: 10,
          data: this.citynamelist,
        },
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
            data: [
              { value: 10, name: "rose1" },
              { value: 5, name: "rose2" },
              { value: 15, name: "rose3" },
              { value: 25, name: "rose4" },
              { value: 20, name: "rose5" },
              { value: 35, name: "rose6" },
              { value: 30, name: "rose7" },
              { value: 40, name: "rose8" },
            ],
          },
        ],
      };
      myChart.setOption(option);

      window.addEventListener("resize", function () {
        myChart.resize();
      });
    },

    drawMap() {
      var myChart = echarts.init(document.getElementById("map"));
      var geoCoordMap = {
        // 上海: [121.4648, 31.2891],
        // 丽水: [119.5642, 28.1854],
        // 乌鲁木齐: [87.9236, 43.5883],
        // 佛山: [112.8955, 23.1097],
        // 保定: [115.0488, 39.0948],
        // 兰州: [103.5901, 36.3043],
        // 包头: [110.3467, 41.4899],
        // 北京: [116.4551, 40.2539],
        // 北海: [109.314, 21.6211],
        // 南京: [118.8062, 31.9208],
        // 南宁: [108.479, 23.1152],
        // 南昌: [116.0046, 28.6633],
        // 南通: [121.1023, 32.1625],
        // 厦门: [118.1689, 24.6478],
        // 台州: [121.1353, 28.6688],
        // 合肥: [117.29, 32.0581],
        // 呼和浩特: [111.4124, 40.4901],
        // 咸阳: [108.4131, 34.8706],
        // 哈尔滨: [127.9688, 45.368],
        // 唐山: [118.4766, 39.6826],
        // 嘉兴: [120.9155, 30.6354],
        // 大同: [113.7854, 39.8035],
        // 大连: [122.2229, 39.4409],
        // 天津: [117.4219, 39.4189],
        // 太原: [112.3352, 37.9413],
        // 威海: [121.9482, 37.1393],
        // 宁波: [121.5967, 29.6466],
        // 宝鸡: [107.1826, 34.3433],
        // 宿迁: [118.5535, 33.7775],
        // 常州: [119.4543, 31.5582],
        // 广州: [113.5107, 23.2196],
        // 廊坊: [116.521, 39.0509],
        // 延安: [109.1052, 36.4252],
        // 张家口: [115.1477, 40.8527],
        // 徐州: [117.5208, 34.3268],
        // 德州: [116.6858, 37.2107],
        // 惠州: [114.6204, 23.1647],
        // 成都: [103.9526, 30.7617],
        // 扬州: [119.4653, 32.8162],
        // 承德: [117.5757, 41.4075],
        // 拉萨: [91.1865, 30.1465],
        // 无锡: [120.3442, 31.5527],
        // 日照: [119.2786, 35.5023],
        // 昆明: [102.9199, 25.4663],
        // 杭州: [119.5313, 29.8773],
        // 枣庄: [117.323, 34.8926],
        // 柳州: [109.3799, 24.9774],
        // 株洲: [113.5327, 27.0319],
        // 武汉: [114.3896, 30.6628],
        // 汕头: [117.1692, 23.3405],
        // 江门: [112.6318, 22.1484],
        // 沈阳: [123.1238, 42.1216],
        // 沧州: [116.8286, 38.2104],
        // 河源: [114.917, 23.9722],
        // 泉州: [118.3228, 25.1147],
        // 泰安: [117.0264, 36.0516],
        // 泰州: [120.0586, 32.5525],
        // 济南: [117.1582, 36.8701],
        // 济宁: [116.8286, 35.3375],
        // 海口: [110.3893, 19.8516],
        // 淄博: [118.0371, 36.6064],
        // 淮安: [118.927, 33.4039],
        // 深圳: [114.5435, 22.5439],
        // 清远: [112.9175, 24.3292],
        // 温州: [120.498, 27.8119],
        // 渭南: [109.7864, 35.0299],
        // 湖州: [119.8608, 30.7782],
        // 湘潭: [112.5439, 27.7075],
        // 滨州: [117.8174, 37.4963],
        // 潍坊: [119.0918, 36.524],
        // 烟台: [120.7397, 37.5128],
        // 玉溪: [101.9312, 23.8898],
        // 珠海: [113.7305, 22.1155],
        // 盐城: [120.2234, 33.5577],
        // 盘锦: [121.9482, 41.0449],
        // 石家庄: [114.4995, 38.1006],
        // 福州: [119.4543, 25.9222],
        // 秦皇岛: [119.2126, 40.0232],
        // 绍兴: [120.564, 29.7565],
        // 聊城: [115.9167, 36.4032],
        // 肇庆: [112.1265, 23.5822],
        // 舟山: [122.2559, 30.2234],
        // 苏州: [120.6519, 31.3989],
        // 莱芜: [117.6526, 36.2714],
        // 菏泽: [115.6201, 35.2057],
        // 营口: [122.4316, 40.4297],
        // 葫芦岛: [120.1575, 40.578],
        // 衡水: [115.8838, 37.7161],
        // 衢州: [118.6853, 28.8666],
        // 西宁: [101.4038, 36.8207],
        // 西安: [109.1162, 34.2004],
        // 贵阳: [106.6992, 26.7682],
        // 连云港: [119.1248, 34.552],
        // 邢台: [114.8071, 37.2821],
        // 邯郸: [114.4775, 36.535],
        // 郑州: [113.4668, 34.6234],
        // 鄂尔多斯: [108.9734, 39.2487],
        // 重庆: [107.7539, 30.1904],
        // 金华: [120.0037, 29.1028],
        // 铜川: [109.0393, 35.1947],
        // 银川: [106.3586, 38.1775],
        // 镇江: [119.4763, 31.9702],
        // 长春: [125.8154, 44.2584],
        // 长沙: [113.0823, 28.2568],
        // 长治: [112.8625, 36.4746],
        // 阳泉: [113.4778, 38.0951],
        // 青岛: [120.4651, 36.3373],
        // 韶关: [113.7964, 24.7028],
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

      var XAData = [
        [{ name: "西安" }, { name: "拉萨", value: 100 }],
        [{ name: "西安" }, { name: "上海", value: 100 }],
        [{ name: "西安" }, { name: "广州", value: 100 }],
        [{ name: "西安" }, { name: "西宁", value: 100 }],
        [{ name: "西安" }, { name: "银川", value: 100 }],
      ];

      var XNData = [
        [{ name: "西宁" }, { name: "北京", value: 100 }],
        [{ name: "西宁" }, { name: "上海", value: 100 }],
        [{ name: "西宁" }, { name: "广州", value: 100 }],
        [{ name: "西宁" }, { name: "西安", value: 100 }],
        [{ name: "西宁" }, { name: "银川", value: 100 }],
      ];

      var YCData = [
        [{ name: "拉萨" }, { name: "济南", value: 100 }],
        [{ name: "拉萨" }, { name: "哈尔滨", value: 100 }],
        [{ name: "银川" }, { name: "上海", value: 100 }],
        [{ name: "银川" }, { name: "西安", value: 100 }],
        [{ name: "银川" }, { name: "西宁", value: 100 }],
      ];

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
        console.log("res[1]:", res[1]);
        return res;
      };

      var color = ["#a6c84c", "#ffa022", "#46bee9"]; //航线的颜色
      var series = [];
      [
        ["西安", XAData],
        ["西宁", XNData],
        ["银川", YCData],
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

/* @font-face {
    font-family: 'electronicFont';
    src: url('../../assets/layui/font/DS-DIGIT.TTF');
} */

#simulationMap {
  background: url(../../assets/img/bg.jpg) no-repeat top center;
  line-height: 1.15;
  height: 655px;
  width: 100%;
  background-size: 100% 100%;
}

header {
  position: relative;
  height: 1.25rem;
  background: url(../../assets/img/head_bg.png) no-repeat;
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
  line-height: 0.6rem;
  text-align: center;
  color: #fff;
  font-size: 20px;
  font-weight: 400;
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
  height: 280px;
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
  color: #ffeb7b;
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
  color: rgba(255, 255, 255, 0.7);
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
  height: 480px;
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

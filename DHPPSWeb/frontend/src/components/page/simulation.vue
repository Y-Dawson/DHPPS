<template>
  <div id="simulation">
    <div class="layui-layout layui-layout-admin">
      <div class="layui-header">
        <div class="layui-logo">LOGO</div>
        <div class="layui-logotext">高传染性疾病预测系统</div>
        <!-- <div class="layui-logo">高传染性疾病预测系统</div> -->
        <!-- 头部区域（可配合layui已有的水平导航） -->
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
    </div>

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
        <span class="title">已创建：</span>
        <li>
          <div>
            <span class="little-title">城市列表：</span>
            <li id="city_inf" v-for="city in city_inf" :key="city">
              {{ city[day] }}
            </li>
          </div>
        </li>
        <li>
          <div>
            <span class="little-title">道路列表：</span>
            <li id="road_inf" v-for="road in road_di" :key="road">
              {{ road }}
            </li>
          </div>
        </li>
      </ul>

      <ul class="img-list">
        <li v-for="o in citycnt + 100" :key="o">
          <div :id="'ci' + o" class="city" style="left: 10000px; top: 10000px">
            <img
              src="../../assets/layui/images/city.gif"
              alt=""
              @click="outp('ci' + o)"
            />
            <div class="city-infor">
              <div v-for="j in row_cnt[o]" :key="j">
                <span v-for="k in people_cnt[o][j]" :key="k" class="text item">
                  <i
                    :id="'i' + o + j + k"
                    class="layui-icon layui-icon-template-1 cityicon"
                  ></i>
                </span>
              </div>
            </div>
          </div>
        </li>

        <!-- <li>
          <div id="ci1" class="city" style="left: 300px; top: 300px">
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci1_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci1_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci1_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci2"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci2_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci2_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci2_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci3"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci3_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci3_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci3_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci4"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci4_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci4_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci4_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci5"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci5_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci5_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci5_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci6"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci6_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci6_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci6_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci7"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci7_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci7_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci7_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci8"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci8_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci8_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci8_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci9"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci9_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci9_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci9_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li>

        <li>
          <div
            id="ci10"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
          >
            <img src="../../assets/layui/images/city.gif" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <span>总人口：{{ ci10_population[day] }}</span>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <span>总感染人数：{{ ci10_totalInfected[day] }}</span>
              </el-form-item>

              <el-form-item>
                <span>新增感染人数：{{ ci10_newInfected[day] }}</span>
              </el-form-item>
            </div>
          </div>
        </li> -->
      </ul>

      <ul class="line_list">
        <li>
          <div
            id="line1"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          >
            <span></span>
            <span></span>
          </div>
        </li>

        <li>
          <div
            id="line2"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line3"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line4"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line5"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line6"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line7"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line8"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line9"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line10"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line11"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
        </li>

        <li>
          <div
            id="line12"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
          ></div>
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

<script>
import Global from "../../global_vue";

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
      cityname: [],

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
    this.params = JSON.parse(this.$route.query.params);

    console.log("用户ID：", this.params.userId);
    console.log("案例名：", this.params.caseName);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.InitCityData);
    console.log("道路信息：", this.params.InitRoadData);
    console.log("城市坐标：", this.params.CityPosition);
    console.log("每日病例：", this.params.DailyInfected.data.DailyForecastData);
    var foreData = this.params.DailyInfected.data.DailyForecastData;

    this.userId = this.params.userId;
    this.casename = this.params.caseName;
    this.citycnt = this.params.citynum;
    this.linecnt = this.params.roadnum;
    this.city_information = this.params.InitCityData;
    this.road_inf = this.params.InitRoadData;
    this.city_position = this.params.CityPosition;
    this.day_num = parseInt(this.params.Daynum);
    this.daily_step = 100 / this.day_num;
    console.log("模拟天数：", this.params.Daynum);
    console.log("每日跨度：", this.daily_step);

    for (var i = 0; i < parseInt(this.params.Daynum); i++) {
      for (var j = 0; j < parseInt(this.params.citynum); j++) {
        this.AddInformation(
          foreData[i][j]["cityName"],
          foreData[i][j]["population"],
          foreData[i][j]["dailyinfected"],
          foreData[i][j]["infected"]
        );
      }
    }

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

    this.row_cnt.push(1);

    console.log("citynum", this.citycnt);
    console.log("c3inf", this.ci3_totalInfected);

    for (var i = 0; i < parseInt(this.params.citynum); i++) {
      var pop = parseInt(foreData[0][i]["population"]);
      pop = parseInt(pop / 100);
      var temp = parseInt(pop / 8);
      if (pop % 8 != 0) {
        temp += 1;
      }
      this.row_cnt.push(temp);
      var newb = new Array();
      newb.push(1);
      for (var j = 1; j <= temp; j++) {
        if (j < temp) {
          newb.push(8);
        } else {
          var le = pop - (temp - 1) * 8;
          newb.push(le);
        }
      }
      this.people_cnt.push(newb);
    }

    this.row_cnt.push(0);
    console.log("rc", this.row_cnt);

    var cnt = 0;
    for (var j in this.params.CityPosition) {
      var te = this.params.CityPosition[j].split(",");
      console.log("te", te);
      console.log("j", j);
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

      console.log("cityID", cid);
      console.log("cityentity", cityentity);

      cityentity.style.left = x + "px";
      cityentity.style.top = y + "px";

      console.log("cityID", cid);
    }

    for (var j in this.params.InitRoadData) {
      console.log(this.params.InitRoadData[j]);
      var ri = this.params.InitRoadData[j].split(",");
      console.log(ri);
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
      console.log(cid1, cid2);

      this.DrawLine(cid1, cid2);
    }

    console.log("c1_inf：", this.ci1_population);
  },

  methods: {
    StopSimulation(ss) {
      if (this.ss == true) {
        console.log("返回设置参数界面");
        this.ss = false;
        this.$router.push({
          path: "/setting",
          query: {
            params: JSON.stringify({
              userId: this.userId,
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
      console.log("day：", this.day);
      this.changeColor(this.day);
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

      console.log("tcx1:", tcx1);
      console.log("tcy1:", tcy1);
      console.log("tcx2:", tcx2);
      console.log("tcy2:", tcy2);

      const dx = Math.abs(tcx1 - tcx2);
      const dy = Math.abs(tcy1 - tcy2);
      var dis = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

      console.log("dis:", dis);

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
      ll.style.left = (ttcx1 + ttcx2) / 2 - parseInt(dis) / 2 + 20 + "px";
      ll.style.top = (ttcy1 + ttcy2) / 2 + 50 + "px";
      ll.style.transition = "width 2s";
      ll.style.width = parseInt(dis) + "px";
      ll.style.transform = "rotate(" + rotang + "deg)";
      linecnt += 1;
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
      if (n == "G") return "ci10";
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
      if (n == "G") return 10;
      if (n == "K") return 11;
      if (n == "L") return 12;
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
        this.ci3_population.push(popu);
        this.ci3_totalInfected.push(inf);
        this.ci3_newInfected.push(dinf);
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
        console.log("ccnt", ccnt);
        console.log("nowcnt", nowcnt);
        console.log("typeofnowcnt", typeof nowcnt);
        console.log("row_cnt[nowcnt]", this.row_cnt[2]);
        console.log("row_cnt[nowcnt]", this.row_cnt[nowcnt]);
        for (var j = 1; j <= this.row_cnt[nowcnt]; j++) {
          if (j < this.row_cnt[nowcnt]) {
            for (var k = 1; k <= 8; k++) {
              var iid = "i" + ccnt + j + k;
              console.log("iid",iid);
              var iidentity = document.getElementById(iid);
              console.log("iidentity", iidentity);
              iidentity.style.color = "green";
              // console.log("iid", iid);
            }
          } else {
            // console.log("换行");
            for (var k = 1; k <= this.people_cnt[nowcnt][j]; k++) {
              var iid = "i" + ccnt + j + k;
              var iidentity = document.getElementById(iid);
              // console.log("iidentity", iidentity);
              iidentity.style.color = "green";
              // console.log("iid", iid);
            }
          }
        }

        if (ccnt == 1) {
          var inf_cnt = parseInt(this.ci1_totalInfected[index]);
          inf_cnt = parseInt(inf_cnt / 100);
          console.log("tot", this.ci1_totalInfected[index]);
          console.log("inf_cnt", inf_cnt);

          for (var j = 1; j <= this.row_cnt[nowcnt]; j++) {
            if (inf_cnt > 8) {
              for (var k = 1; k <= 8; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              inf_cnt -= 8;
            } else {
              for (var k = 1; k <= inf_cnt; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              break;
            }
          }
        }

        if (ccnt == 2) {
          var inf_cnt = parseInt(this.ci2_totalInfected[index]);
          inf_cnt = parseInt(inf_cnt / 100);
          console.log("tot", this.ci2_totalInfected[index]);
          console.log("inf_cnt", inf_cnt);

          for (var j = 1; j <= this.row_cnt[nowcnt]; j++) {
            if (inf_cnt > 8) {
              for (var k = 1; k <= 8; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              inf_cnt -= 8;
            } else {
              for (var k = 1; k <= inf_cnt; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              break;
            }
          }
        }

        if (ccnt == 3) {
          var inf_cnt = parseInt(this.ci3_totalInfected[index]);
          inf_cnt = parseInt(inf_cnt / 100);
          console.log("tot", this.ci3_totalInfected[index]);
          console.log("inf_cnt", inf_cnt);

          console.log("row_cnt", this.row_cnt);
          console.log("row_cnt[ccnt]", this.row_cnt[nowcnt]);

          for (var j = 1; j <= this.row_cnt[nowcnt]; j++) {
            console.log("可执行");
            if (inf_cnt > 8) {
              for (var k = 1; k <= 8; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              inf_cnt -= 8;
            } else {
              for (var k = 1; k <= inf_cnt; k++) {
                var iid = "i" + ccnt + j + k;
                var iidentity = document.getElementById(iid);
                console.log("iidentity", iidentity);
                iidentity.style.color = "red";
              }
              break;
            }
          }
        }
      }
    },

    outp(data) {
      alert(data);
    },
  },
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";

/* body {
  overflow: hidden;
} */

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
  box-shadow: 2px 2px rgba(0, 0, 0, 0.2);
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
  background-color: rgb(241, 245, 253);
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
  background-color: skyblue;
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
  width: 220px;
  height: 655px;
  background-color: rgb(241, 245, 253);
  border: 1px solid rgb(204, 204, 204);
  border-radius: 10px;
  box-shadow: 0 0 2px 2px rgba(0, 0, 0, 0.2);
}

.city-list .title {
  display: block;
  font-size: 24px;
  margin-left: 5px;
  margin-bottom: 10px;
}

.city-list div {
  margin-left: 10px;
  width: 160px;
  height: 300px;
  background-color: rgb(241, 245, 253);
  border: 1px solid rgb(204, 204, 204);
  border-radius: 10px;
  box-shadow: 2px 2px rgba(0, 0, 0, 0.2);
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

.img-list .city {
  display: block;
  position: absolute;
  /* left: 5000px;
  top: 3000px; */
}

.img-list .city .city-infor {
  height: 185px;
  width: 190px;
  margin-top: -220px;
  margin-left: 60px;
  border: 1px solid rgb(187, 187, 187);
  background-color: #ffffff;
  z-index: 9999;
}

.img-list .city img {
  height: 75px;
  width: 75px;
}

.line_list .road_line {
  display: block;
  position: absolute;
  height: 5px;
  background-color: #000;
  overflow: hidden;
}

.block {
  position: absolute;
  width: 800px;
  margin-left: 325px;
  margin-top: 550px;
}

.cityicon {
  margin-right: 8px;
}

.road_line span {
  position: absolute;
  display: block;
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
</style>

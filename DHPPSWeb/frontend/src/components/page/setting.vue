<template>
  <div id="setting">
    <header>
      <h1>自定模式</h1>
      <div class="toDIY">
        <button @click="toMapModel">地图模式</button>
      </div>

      <div class="toMy">
        <router-link :to="{ path: '/Userprofile' }" style="margin-left: 10px; float: left"
          >个人中心</router-link
        >
      </div>
    </header>

    <canvas
      id="myCanvas"
      width="1320"
      height="660"
      style="border: 1px solid #c3c3c3"
      ref="canvas"
      @click="ShowCity"
    ></canvas>

    <el-form
      ref="cityFormRef"
      :model="cityForm"
      :rules="cityFormRule"
      style="absolute"
      @submit.native.prevent
    >
      <ul class="tools-wrapper">
        <li>
          <el-form-item class="new-pointer">
            <button
              type="primary"
              v-bind:class="{ active1: np }"
              @click="
                np = !np;
                NewPointer(np);
              "
            >
              <i class="layui-icon layui-icon-add-circle"></i>
              <span>新建节点</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="connect-pointer">
            <button
              type="primary"
              v-bind:class="{ active1: cp }"
              @click="
                cp = !cp;
                ConnectPointer(cp);
              "
            >
              <i class="layui-icon layui-icon-release"></i>
              <span>连接节点</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="delete-pointer">
            <button
              type="primary"
              v-bind:class="{ active1: dp }"
              @click="
                dp = !dp;
                DeletePointer(dp);
              "
            >
              <i class="layui-icon layui-icon-delete"></i>
              <span>删除节点</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="delete-road">
            <button
              type="primary"
              v-bind:class="{ active1: dr }"
              @click="
                dr = !dr;
                DeleteRoad(dr);
              "
            >
              <i class="layui-icon layui-icon-fonts-clear"></i>
              <span>删除道路</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="begin-simulate">
            <button
              type="primary"
              v-bind:class="{ active1: bs }"
              @click="
                bs = !bs;
                BeginSimulation(bs);
              "
            >
              <i class="layui-icon layui-icon-play"></i>
              <span>开始模拟</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="save-case">
            <button
              type="primary"
              v-bind:class="{ active1: sc }"
              @click="
                sc = !sc;
                SaveCase(sc);
              "
            >
              <i class="layui-icon layui-icon-log"></i>
              <span>保存案例</span>
            </button>
          </el-form-item>
        </li>
        <li class="line"></li>
        <li>
          <el-form-item class="my-case">
            <button
              type="primary"
              v-bind:class="{ active1: mc }"
              @click="
                mc = !mc;
                MyCase(mc);
              "
            >
              <i class="layui-icon layui-icon-user"></i>
              <span>我的案例</span>
            </button>
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
          <div class="panel">
            <h2>城市信息</h2>
            <div class="chart" id="bar"></div>
          </div>
          <!-- <div>
            <span class="little-title">城市列表：</span>
            <li id="city_inf" v-for="city in city_po" :key="city">
              {{ city }}
            </li>
          </div> -->
        </li>
        <li>
          <div class="panel">
            <h2>道路信息</h2>
            <div class="chart" id="threebar"></div>
            <!-- <span class="little-title">道路列表：</span>
            <li id="city_inf" v-for="road in road_di" :key="road">
              {{ road }}
            </li> -->
          </div>
        </li>
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
            @click="DeleteRoad('line1')"
          ></div>
        </li>

        <li>
          <div
            id="line2"
            class="road_line"
            :style="{
              left: lineleft + 'px',
              top: linetop + 'px',
            }"
            @click="DeleteRoad('line2')"
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
            @click="DeleteRoad('line3')"
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
            @click="DeleteRoad('line4')"
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
            @click="DeleteRoad('line5')"
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
            @click="DeleteRoad('line6')"
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
            @click="DeleteRoad('line7')"
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
            @click="DeleteRoad('line8')"
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
            @click="DeleteRoad('line9')"
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
            @click="DeleteRoad('line10')"
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
            @click="DeleteRoad('line11')"
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
            @click="DeleteRoad('line12')"
          ></div>
        </li>
      </ul>

      <ul class="img-list">
        <li>
          <div
            id="ci1"
            class="city"
            :style="{
              left: cityForm.cityleft + 'px',
              top: cityForm.citytop + 'px',
            }"
            @click="
              ConnectCity('ci1');
              DeleteCity('ci1');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf1">
              <!-- <el-form-item prop="cityName">
                <el-input
                  v-model="cityForm.cityName"
                  placeholder="城市名"
                ></el-input>
              </el-form-item> -->

              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci1')"
                  :disabled="isdisabled1"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci2');
              DeleteCity('ci2');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf2">
              <!-- <el-form-item prop="cityName">
                <el-input
                  v-model="cityForm.cityName"
                  placeholder="城市名"
                ></el-input>
              </el-form-item> -->

              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci2')"
                  :disabled="isdisabled2"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci3');
              DeleteCity('ci3');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf3">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci3')"
                  :disabled="isdisabled3"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci4');
              DeleteCity('ci4');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf4">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci4')"
                  :disabled="isdisabled4"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci5');
              DeleteCity('ci5');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf5">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci5')"
                  :disabled="isdisabled5"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci6');
              DeleteCity('ci6');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf6">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci6')"
                  :disabled="isdisabled6"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci7');
              DeleteCity('ci7');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf7">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci7')"
                  :disabled="isdisabled7"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci8');
              DeleteCity('ci8');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf8">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci8')"
                  :disabled="isdisabled8"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci9');
              DeleteCity('ci9');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf9">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci9')"
                  :disabled="isdisabled9"
                  >确 认</el-button
                >
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
            @click="
              ConnectCity('ci10');
              DeleteCity('ci10');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor" id="cityinf10">
              <el-form-item prop="population" class="set_input">
                <el-input v-model="cityForm.population" placeholder="城市人口"></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected" class="set_input">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item class="set_button">
                <el-button
                  type="primary"
                  @click="ConfirmCity('ci10')"
                  :disabled="isdisabled10"
                  >确 认</el-button
                >
              </el-form-item>
            </div>
          </div>
        </li>
      </ul>
    </el-form>
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
import g_Global from "../../global_vue.js";
// import { flexible } from "../../assets/js/flexible.js";
import { jquery } from "../../assets/js/jquery.js";
var echarts = require("echarts");
import "../../../node_modules/echarts/lib/chart/map/china.js";

var citycnt = 1;
var nowcitycnt = 1;
var linecnt = 1;
var concnt = 0;
var cn = 0;
var numReg = /^[0-9]*$/;
var numRe = new RegExp(numReg);
var cityUsed = [];
var cName = [];
var cPeople = [];
var cInf = [];

export default {
  data() {
    return {
      fits: ["fill"],
      url: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",

      userId: "",

      np: false,
      cp: false,
      dp: false,
      dr: false,
      bs: false,
      sc: false,
      mc: false,

      alreadyConfirm: true,

      cid1: "",
      cid2: "",
      cityx1: 0,
      cityy1: 0,
      cityx2: 0,
      cityy2: 0,

      isdisabled1: false,
      isdisabled2: false,
      isdisabled3: false,
      isdisabled4: false,
      isdisabled5: false,
      isdisabled6: false,
      isdisabled7: false,
      isdisabled8: false,
      isdisabled9: false,
      isdisabled10: false,
      showed: true,
      // cityleft: g_Global.cityleft,
      // citytop: g_Global.citytop,
      lineleft: g_Global.lineleft,
      linetop: g_Global.linetop,

      cityForm: {
        // cityName: "",
        population: "",
        beginInfected: "",
        distance: "",
        traffic: "",
        // cityleft: g_Global.cityleft,
        // citytop: g_Global.citytop,
        // cityleft: this.$root.cityleft,
        // citytop: this.$root.citytop
        cityleft: g_Global.cityleft,
        citytop: g_Global.citytop,
      },
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

      cityname: [],
      citypeople: [],
      cityInf: [],
      roadVol: [],

      cityFormRule: {
        // cityName: [
        //   { required: true, message: "请输入城市名", trigger: "blur" },
        //   {
        //     min: 3,
        //     max: 15,
        //     message: "长度在3到15个字符之间",
        //     trigger: "blur",
        //   },
        // ],
        population: [
          { required: true, message: "请输入城市人数", trigger: "blur" },
          {
            min: 1,
            max: 15000,
            message: "城市人数在1到15000之间",
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
    console.log("案例名：", this.params.caseName);
    // console.log("类型：", typeof this.params.casename);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.InitCityData);
    console.log("道路信息：", this.params.InitRoadData);
    console.log("城市坐标：", this.params.CityPosition);
    // this.userId = this.params.userId;

    cityUsed = [];
    cName = [];
    cPeople = [];
    cInf = [];
    for (var i = 0; i <= 10; i++) {
      //每次调整这个数组里的东西，然后存储信息也是分开存储，在需要的时候按照这个数组的布尔值要
      //初始化、新增城市、删除城市
      cityUsed.push(false);
      cName.push(1);
      cPeople.push(1);
      cInf.push(1);
      this.SetButtonToFalse(i);
    }
    console.log("this.cityused", cityUsed);

    citycnt = 1;
    nowcitycnt = 1;
    linecnt = 1;
    if (this.params.caseName != 999) {
      console.log("从模拟界面返回");
      citycnt = this.params.citynum + 1;
      nowcitycnt = citycnt;
      linecnt = 1;
      var cnt = 0;
      for (var j in this.params.CityPosition) {
        var te = this.params.CityPosition[j].split(",");
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
        cityentity.style.left = x + "px";
        cityentity.style.top = y + "px";
        var nu = this.GetNum(cid);
        nu = parseInt(nu);
        this.SetButton(nu);

        citycnt = nu + 1;
        nowcitycnt = citycnt;
      }

      for (var j in this.params.InitRoadData) {
        // console.log(this.params.Initroaddata[j]);
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

      console.log("roadVol", this.roadVol);

      for (var j in this.params.InitCityData) {
        var ci = this.params.InitCityData[j].split(",");
        var tt, cityna, initpo, initIn;
        cnt = 0;
        for (var k in ci) {
          cnt += 1;
          if (cnt == 1) {
            tt = ci[k].split(":");
            cityna = tt[1];
          }
          if (cnt == 2) {
            tt = ci[k].split(":");
            initpo = tt[1];
          }
          if (cnt == 3) {
            tt = ci[k].split(":");
            initIn = tt[1];
          }
        }
        var s = cityna + ": 总人口:" + initpo;
        this.city_po.push(s);
        s = "初始感染人数:" + initIn;
        this.city_po.push(s);

        var n = this.GetNum(cityna);

        cName[n] = cityna;
        cPeople[n] = initpo;
        cInf[n] = initIn;
        cityUsed[n] = true;

        this.SetButtonToFalse(n);

        this.cityname.push(cityna);
        this.citypeople.push(initpo);
        this.cityInf.push(initIn);
      }

      this.DrawMap();
      this.DrawRoadMap();
    }
  },

  methods: {
    NewPointer(np) {
      this.correctCity();
      concnt = 0;

      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
      if (np == true) {
        console.log("我可以新建节点了");
      }
    },

    ConnectPointer(cp) {
      console.log("点了");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    DeletePointer(dp) {
      console.log("可以删除节点了");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.cp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    DeleteRoad(dr) {
      console.log("可以删除边了");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.cp = false;
      this.dp = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    BeginSimulation(bs) {
      console.log("开始模拟");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.sc = false;
      this.mc = false;

      if (nowcitycnt == 1) {
        this.$message({
          type: "warning",
          message: "您还未进行任何创建",
        });
        this.bs = false;
        return;
      }

      this.BeginToSimulation().then((response) => {});
    },

    SaveCase(sc) {
      console.log("保存案例");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.mc = false;

      if (nowcitycnt == 1) {
        this.$message({
          type: "warning",
          message: "您还未进行任何创建",
        });
        this.sc = false;
        return;
      }

      this.SaveConfirm().then((response) => {});
    },

    MyCase(mc) {
      console.log("我的案例");
      this.correctCity();
      concnt = 0;

      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;

      this.$confirm(
        "请确保您已保存案例，此操作将会丢失您在此页面上的所有编辑内容, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      )
        .then(() => {
          this.$router.push({
            path: "/UserCase",
          });
        })
        .catch(() => {
          this.mc = false;
          this.$message({
            type: "info",
            message: "已取消跳转",
          });
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
      ll.style.width = parseInt(dis) + "px";
      ll.style.transform = "rotate(" + rotang + "deg)";
      linecnt += 1;

      console.log("画了这条线了：", linecnt);
    },

    DrawMap() {
      console.log("画个柱状图");

      var myChart = echarts.init(document.getElementById("bar"));

      var seriesLabel = {
        normal: {
          show: true,
          textBorderColor: "#333",
          textBorderWidth: 2,
        },
      };

      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
        },
        legend: {
          data: ["总人口", "感染人数"],
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
            data: this.citypeople,
            label: seriesLabel,
          },
          {
            name: "感染人数",
            type: "bar",
            label: seriesLabel,
            data: this.cityInf,
          },
        ],
      };

      myChart.setOption(option);
    },

    DrawRoadMap() {
      console.log("roadVol", this.roadVol);

      var myChart = echarts.init(document.getElementById("threebar"));

      console.log("myChart", myChart);

      console.log("cityname", this.cityname);

      console.log("画个3D柱状图");

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
      console.log("快画完了");
      myChart.setOption(option);
      console.log("画完了");
    },

    BeginToSimulation() {
      this.$prompt("请输入模拟天数", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "模拟天数格式不正确",
      })
        .then(({ value }) => {
          var d = parseInt(value);
          if (d < 5 || d > 100) {
            this.$alert("模拟天数应在5~100内", "模拟失败", {
              confirmButtonText: "确定",
              callback: (action) => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`,
                });
              },
            });
            this.bs = false;
            return;
          }

          this.sc = false;

          var myFormData = new FormData();

          myFormData.append("userId", this.userId);

          myFormData.append("caseName", 99);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var loopcnt = 0;
          var trcitycnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt == 1) {
              cn = this.city_po[cid].substring(0, 1);
              initpop = this.city_po[cid].substring(7);
            }
            if (loopcnt == 2) {
              initinfect = this.city_po[cid].substring(7);
              trcitycnt += 1;
              var s =
                "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
              city_infor.push(s);
              loopcnt = 0;
            }
          }

          myFormData.append("citynum", trcitycnt);

          var roadcnt = 0;
          var road_inf = [];
          for (var rid in this.road_di) {
            roadcnt += 1;
            var departure = this.road_di[rid].substring(0, 1);
            var destination = this.road_di[rid].substring(2, 3);
            var volume = this.road_di[rid].substring(4);
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
          myFormData.append("caseMode", 1);

          myFormData.append("InitCityData", city_infor);

          if (roadcnt == 0) {
            myFormData.append("InitRoadData", "NULL");
          } else {
            myFormData.append("InitRoadData", road_inf);
          }

          var city_position = [];
          loopcnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt % 2 == 1) {
              var cityName = this.city_po[cid].substring(0, 1);
              var cityID = this.GetID(cityName);

              console.log("cityName:" + cityName + " cityID:" + cityID);

              var c = document.getElementById(cityID);
              var x = c.style.left.substring(0, c.style.left.length - 2);
              var y = c.style.top.substring(0, c.style.top.length - 2);
              var s = "cityname:" + cityName + ",x:" + x + ",y:" + y;
              city_position.push(s);
            }
          }
          myFormData.append("CityPosition", city_position);

          myFormData.append("daynum", parseInt(value) + 1);

          for (var value of myFormData.values()) {
            console.log(value);
          }

          axios
            .post("/apis/backend/startSimulate/", myFormData)
            .then((response) => {
              alert(JSON.stringify(response));
              // alert("开始模拟");
              this.$router.push({
                path: "/simulation",
                query: {
                  params: JSON.stringify({
                    caseName: 99,
                    citynum: trcitycnt,
                    roadnum: roadcnt,
                    InitCityData: city_infor,
                    InitRoadData: road_inf,
                    CityPosition: city_position,
                    Daynum: value,
                    DailyInfected: response,
                  }),
                },
              });
            })
            .catch(function (error) {
              // alert(JSON.stringify(response));
              // alert("发送失败");
            });
        })
        .catch(() => {
          this.bs = false;
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    SaveConfirm() {
      this.$prompt("请输入此案例名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[\u4e00-\u9fa5_a-zA-Z0-9]{1,3}$/,
        inputErrorMessage: "案例名称可为汉字、英文字母和数字，长度为1到3个字符",
      })
        .then(({ value }) => {
          this.sc = false;

          var myFormData = new FormData();

          myFormData.append("userId", this.userId);

          myFormData.append("caseName", value);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var loopcnt = 0;
          var trcitycnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt == 1) {
              cn = this.city_po[cid].substring(0, 1);
              initpop = this.city_po[cid].substring(7);
            }
            if (loopcnt == 2) {
              initinfect = this.city_po[cid].substring(7);
              trcitycnt += 1;
              var s =
                "cityname:" + cn + ",initpop:" + initpop + ",initinfect:" + initinfect;
              city_infor.push(s);
              loopcnt = 0;
            }
          }
          myFormData.append("citynum", trcitycnt);

          var roadcnt = 0;
          var road_inf = [];
          for (var rid in this.road_di) {
            roadcnt += 1;
            var departure = this.road_di[rid].substring(0, 1);
            var destination = this.road_di[rid].substring(2, 3);
            var volume = this.road_di[rid].substring(4);
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
          myFormData.append("caseMode", 1);

          myFormData.append("InitCityData", city_infor);

          if (roadcnt == 0) {
            myFormData.append("InitRoadData", "NULL");
          } else {
            myFormData.append("InitRoadData", road_inf);
          }

          var city_position = [];
          loopcnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt % 2 == 1) {
              var cityName = this.city_po[cid].substring(0, 1);
              var cityID = this.GetID(cityName);

              console.log("cityName:" + cityName + " cityID:" + cityID);

              var c = document.getElementById(cityID);
              var x = c.style.left.substring(0, c.style.left.length - 2);
              var y = c.style.top.substring(0, c.style.top.length - 2);
              var s = "cityname:" + cityName + ",x:" + x + ",y:" + y;
              city_position.push(s);
            }
          }
          myFormData.append("CityPosition", city_position);

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
          this.sc = false;
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    ShowCity(e) {
      window.cityleft = e.pageX;
      window.citytop = e.pageY;
      // g_Global.cityleft = e.pageX;
      // g_Global.citytop = e.pageY;
      this.$set(g_Global, cityleft, e.pageX);
      this.$set(g_Global, citytop, e.pageY);
      if (this.np == true) {
        var nowc = parseInt(this.GetUnused());
        console.log("nowc", nowc);
        if (nowc == 99) {
          this.$message({
            type: "warning",
            message: "您创建的城市已经达到上限，您可以进行模拟、保存案例或者尝试地图模式",
          });
          this.np = false;
          return;
        }

        if (e.pageX < 200 || e.pageY > 640) {
          this.$message({
            type: "warning",
            message: "请您向中部点击，再试一次吧",
          });
          return;
        }

        var c = "ci" + nowc;
        console.log(c);
        var ci = document.getElementById(c);
        var cl = e.pageX - 50;
        var ct = e.pageY - 50;
        ci.style.left = cl + "px";
        ci.style.top = ct + "px";

        console.log("ex", e.pageX);
        console.log("ey", e.pageY);
        console.log("cileft", ci.style.left);
        console.log("citop", ci.style.top);

        this.changePosition(c);

        this.alreadyConfirm = false;
      }
      if (this.cp == true && concnt == 2) {
        console.log("g_concnt：" + concnt);

        var mc = document.getElementById("myCanvas");
        var mctx = mc.getContext("2d");

        mctx.moveTo(this.cityx1, this.cityy1);
        mctx.lineTo(this.cityx2, this.cityy2);

        mctx.beginPath();
        mctx.stroke();
        // this.cp = false;
        concnt = 0;
      }
      // this.set(data.cityForm, "cityleft", e.pageX + "px");
      // this.set(data.cityForm, "citytop", e.pageY + "px");
      this.cityForm.ShowCity = true;
      console.log("cityleft:" + g_Global.cityleft + ", citytop:" + g_Global.citytop);
      console.log("cityleft:" + this.cityleft + ", citytop:" + this.citytop);
    },

    ConfirmRoad(tcx1, tcy1, tcx2, tcy2, dx, dy, dis) {
      var tra = 0;
      console.log("输入人流量");
      this.$prompt("请输入此路人流量（1-100）", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "人流量格式不正确",
      })
        .then(({ value }) => {
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
            concnt = 0;
            this.cp = false;
            return;
          }

          var road_inf = this.road_c1 + "-" + this.road_c2 + ":" + value;
          console.log("road_inf", road_inf);

          var newar1 = new Array();
          var vol = parseInt(value);
          newar1.push(this.road_c1);
          newar1.push(this.road_c2);
          newar1.push(vol);
          this.roadVol.push(newar1);

          var newar2 = new Array();
          var vol = parseInt(value);
          newar2.push(this.road_c2);
          newar2.push(this.road_c1);
          newar2.push(vol);
          this.roadVol.push(newar2);

          console.log("tcx1：" + tcx1);

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
          ll.style.width = parseInt(dis) + "px";
          ll.style.transform = "rotate(" + rotang + "deg)";

          var ci1 = document.getElementById(this.cid1);
          var ci2 = document.getElementById(this.cid2);

          ci1.style.left = ttcx1 + "px";
          ci2.style.left = ttcx2 + "px";
          ci1.style.top = ttcy1 + "px";
          ci2.style.top = ttcy2 + "px";

          // ll.style.position = "absolute";
          // ll.style.zIndex = "2";

          console.log("dis_cos：" + (parseInt(dis) * Math.cos(rotang)) / 2);
          console.log("ll.style.left：" + ll.style.left);
          console.log("ttcx1：" + ttcx1);

          console.log("dis：" + dis);
          console.log("width：" + ll.style.width);

          this.road_di.push(road_inf);

          linecnt += 1;
          this.cp = false;
          concnt = 0;

          this.DrawRoadMap();
        })
        .catch(() => {
          this.cp = false;
          concnt = 0;
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    ConnectCity(e) {
      if (this.cp == true) {
        console.log(e);
        concnt += 1;
        var c = document.getElementById(e);
        console.log("left：" + c.style.left + " top：" + c.style.top);
        // console.log(this.cityForm.cityName);
        if (concnt == 1) {
          this.cid1 = e;
          this.cityx1 = c.style.left;
          this.cityy1 = c.style.top;
          for (var k in this.ci) {
            var k1 = parseInt(k);
            var tc = document.getElementById(this.ci[k1]);
            if (tc.style.left == c.style.left && tc.style.top == c.style.top) {
              this.road_c1 = this.GetName(k1 + 1);
              break;
            }
          }
          // this.road_c1 = c.cityForm.cityName;
          console.log(this.road_c1);
        }
        if (concnt == 2) {
          console.log("第二次了");

          this.cid2 = e;
          this.cityx2 = c.style.left;
          this.cityy2 = c.style.top;

          console.log("cityx1:" + this.cityx1 + ", cityy1:" + this.cityy1);
          console.log("cityx2:" + this.cityx2 + ", cityy2:" + this.cityy2);

          for (var k in this.ci) {
            var k1 = parseInt(k);
            var tc = document.getElementById(this.ci[k1]);
            if (tc.style.left == c.style.left && tc.style.top == c.style.top) {
              this.road_c2 = this.GetName(k1 + 1);
              break;
            }
          }

          if (this.cityx1 == this.cityx2 && this.cityy1 == this.cityy2) {
            this.$alert("请选择两个不同的城市", "连接失败", {
              confirmButtonText: "确定",
              callback: (action) => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`,
                });
              },
            });
            concnt = 0;
            this.cp = false;
            return;
          }

          for (var i in this.road_di) {
            var departure = this.road_di[i].substring(0, 1);
            var destination = this.road_di[i].substring(2, 3);
            // this.road_c1 + "-" + this.road_c2
            if (
              (this.road_c1 == departure && this.road_c2 == destination) ||
              (this.road_c2 == departure && this.road_c1 == destination)
            ) {
              this.$alert("两城市间已存在道路，请选择不同的城市", "连接失败", {
                confirmButtonText: "确定",
                callback: (action) => {
                  this.$message({
                    type: "info",
                    message: `action: ${action}`,
                  });
                },
              });
              concnt = 0;
              this.cp = false;
              return;
            }
          }

          var mc = document.getElementById("myCanvas");
          var mctx = mc.getContext("2d");

          console.log(mc);
          console.log(mctx);

          var cx1 = this.cityx1;
          var tcx1 = cx1.substring(0, cx1.length - 2);
          var cy1 = this.cityy1;
          var tcy1 = cy1.substring(0, cy1.length - 2);
          var cx2 = this.cityx2;
          var tcx2 = cx2.substring(0, cx2.length - 2);
          var cy2 = this.cityy2;
          var tcy2 = cy2.substring(0, cy2.length - 2);
          // var cx1=this.cityx1-'px';
          // console.log(typeof(this.cityx1));

          // mctx.beginPath();

          // mctx.moveTo(tcx1, tcy1);
          // mctx.lineTo(tcx2, tcy2);

          // // mctx.strokeStyle="yellow";
          // mctx.stroke();

          const dx = Math.abs(tcx1 - tcx2);
          const dy = Math.abs(tcy1 - tcy2);
          var dis = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

          // var pu=document.getElementById("dpu");
          // pu.style.visibility="visible";
          this.ConfirmRoad(tcx1, tcy1, tcx2, tcy2, dx, dy, dis).then((response) => {});
        }
      }
    },

    ConfirmDeleteCity(e) {
      this.$confirm("此操作将删除该城市及其相邻的道路, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          console.log("e", e);
          var c = document.getElementById(e);

          var cico = this.GetCode(e);
          console.log("cico", cico);

          var nacnt = 0;
          for (var k in this.cityname) {
            if (cico == this.cityname[k]) {
              nacnt = k;
            }
          }
          console.log(nacnt);
          this.cityname.splice(nacnt, 1);
          this.citypeople.splice(nacnt, 1);
          this.cityInf.splice(nacnt, 1);
          this.DrawMap();

          cn = 0;

          for (var k in this.ci) {
            var k1 = parseInt(k);
            var tc = document.getElementById(this.ci[k1]);
            if (tc.style.left == c.style.left && tc.style.top == c.style.top) {
              break;
            } else if (tc.style.left != 10000 + "px") {
              cn++;
            }
          }

          console.log("cn：" + cn);
          this.city_po.splice(cn * 2, 2);

          for (var i in this.city_po) {
            console.log(this.city_po[i]);
          }

          var city_no = e.substring(2, 3);
          var city_tno = parseInt(city_no);
          console.log("city：" + e);
          var ce = this.GetName(city_tno);
          var cid;

          for (var j in this.road_di) {
            console.log("第一次输出：" + this.road_di[j]);
          }

          var wait_delete = [];

          for (var j in this.road_di) {
            console.log("road_di数组:" + this.road_di[j]);
            var c1 = this.road_di[j].substring(0, 1);
            var c2 = this.road_di[j].substring(2, 3);
            console.log("c1：" + c1 + " c1.type：" + typeof c1);
            console.log("c2：" + c2 + " c2.type：" + typeof c2);
            console.log("ce：" + ce + " ce.type：" + typeof ce);
            console.log("j：" + j);
            if (c1 == ce) {
              cid = this.GetID(c2);
              // this.road_di.splice(j, 1);
              wait_delete.push(j);
            }
            if (c2 == ce) {
              cid = this.GetID(c1);
              wait_delete.push(j);
              // this.road_di.splice(j, 1);
            }

            if (c1 == ce || c2 == ce) {
              console.log("cid", cid);
              var dc = document.getElementById(cid);

              var dcx1 = dc.style.left;
              dcx1 = dcx1.substring(0, dcx1.length - 2);
              var dcx2 = c.style.left;
              dcx2 = dcx2.substring(0, dcx2.length - 2);
              var dcy1 = dc.style.top;
              dcy1 = dcy1.substring(0, dcy1.length - 2);
              var dcy2 = c.style.top;
              dcy2 = dcy2.substring(0, dcy2.length - 2);

              console.log("dcx1：" + dcx1 + " dcy1：" + dcy1);
              console.log("dcx2：" + dcx2 + " dcy2：" + dcy2);

              const dx = Math.abs(dcx1 - dcx2);
              const dy = Math.abs(dcy1 - dcy2);
              var dis = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

              for (var k in this.ri) {
                console.log("lineID：", this.ri[k]);
                var tr = document.getElementById(this.ri[k]);
                var td = parseInt(dis);
                var wi = tr.style.width;
                var tw = wi.substring(0, wi.length - 2);
                var ttw = parseInt(tw);
                console.log("dis：" + td + " width：" + ttw);
                if (td == ttw) {
                  tr.style.left = 10000 + "px";
                  tr.style.top = 10000 + "px";
                }
              }
            }
          }

          var twd = wait_delete.reverse();
          console.log("人流量图变变变");
          for (var j in twd) {
            console.log("删前");
            console.log("road_di", this.road_di);
            console.log("roadVol", this.roadVol);
            this.road_di.splice(twd[j], 1);
            this.roadVol.splice(2 * twd[j], 2);
            console.log("删后");
            console.log("road_di", this.road_di);
            console.log("roadVol", this.roadVol);
          }

          console.log("c", c);

          c.style.left = 10000 + "px";
          c.style.top = 10000 + "px";
          this.dp = false;
          this.$message({
            type: "success",
            message: "删除成功!",
          });

          nowcitycnt--;

          var n = this.GetNum(e);
          cityUsed[n] = false;
          console.log("de_used", cityUsed);

          this.UpdateData();
          this.SetButtonToFalse(n);
          this.DrawMap();
          this.DrawRoadMap();
        })
        .catch(() => {
          this.dp = false;
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

    DeleteCity(e) {
      if (this.dp == true) {
        this.ConfirmDeleteCity(e).then((response) => {});
      }
    },

    DeleteRoad(e) {
      if (this.dr == true) {
        console.log("this.road_di", this.road_di);
        console.log("this.roadVol", this.roadVol);

        var r = document.getElementById(e);
        for (var j in this.road_di) {
          var c1 = this.road_di[j].substring(0, 1);
          var c2 = this.road_di[j].substring(2, 3);
          var cid1 = this.GetID(c1);
          var cid2 = this.GetID(c2);
          var tc1 = document.getElementById(cid1);
          var tc2 = document.getElementById(cid2);

          var dcx1 = tc1.style.left;
          dcx1 = dcx1.substring(0, dcx1.length - 2);
          var dcx2 = tc2.style.left;
          dcx2 = dcx2.substring(0, dcx2.length - 2);
          var dcy1 = tc1.style.top;
          dcy1 = dcy1.substring(0, dcy1.length - 2);
          var dcy2 = tc2.style.top;
          dcy2 = dcy2.substring(0, dcy2.length - 2);

          const dx = Math.abs(dcx1 - dcx2);
          const dy = Math.abs(dcy1 - dcy2);
          var dis = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
          var td = parseInt(dis);

          var wi = r.style.width;
          var tw = wi.substring(0, wi.length - 2);
          var ttw = parseInt(tw);
          if (td == tw) {
            this.road_di.splice(j, 1);
            this.roadVol.splice(2 * j, 2);
            console.log("this.road_di", this.road_di);
            console.log("this.roadVol", this.roadVol);
            break;
          }
        }
        r.style.left = 10000 + "px";
        r.style.top = 10000 + "px";
        this.dr = false;

        this.DrawRoadMap();
      }
    },

    ConfirmCity(e) {
      this.np = false;
      var c = document.getElementById(e);
      // console.log("city_Name:" + this.cityForm.cityName);
      console.log("city_population:" + this.cityForm.population);
      console.log("city_Infected:" + this.cityForm.beginInfected);
      var n = this.GetNum(e);
      var cn = this.GetName(n);

      if (!numRe.test(this.cityForm.population)) {
        this.$message({
          type: "error",
          message: "请输入数字",
        });
        this.cityForm.population = "";
        this.cityForm.beginInfected = "";
        c.style.left = 10000 + "px";
        c.style.top = 10000 + "px";
        return;
      }

      if (!numRe.test(this.cityForm.beginInfected)) {
        this.$message({
          type: "error",
          message: "请输入数字",
        });
        this.cityForm.population = "";
        this.cityForm.beginInfected = "";
        c.style.left = 10000 + "px";
        c.style.top = 10000 + "px";
        return;
      }

      var cy = cn + ": 总人口:" + this.cityForm.population;
      var ipp = parseInt(this.cityForm.population);
      if (ipp < 100 || ipp > 7200) {
        this.$alert("城市人口应在100~7200内", "创建失败", {
          confirmButtonText: "确定",
          callback: (action) => {
            this.$message({
              type: "info",
              message: "请重新创建",
            });
          },
        });
        this.cityForm.population = "";
        this.cityForm.beginInfected = "";
        c.style.left = 10000 + "px";
        c.style.top = 10000 + "px";
        return;
      }

      var cz = "初始感染人数:" + this.cityForm.beginInfected;
      var ibi = parseInt(this.cityForm.beginInfected);
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
        this.cityForm.population = "";
        this.cityForm.beginInfected = "";
        c.style.left = 10000 + "px";
        c.style.top = 10000 + "px";
        return;
      }

      var n = this.GetNum(e);
      cName[n] = cn;
      cPeople[n] = ipp;
      cInf[n] = ibi;
      // this.cityname[n]=cn;
      // this.citypeople[n]=ipp;
      // this.cityInf[n]=ibi;

      // this.cityname.push(cn);
      // this.citypeople.push(this.cityForm.population);
      // this.cityInf.push(this.cityForm.beginInfected);
      this.city_po.push(cy);
      this.city_po.push(cz);

      cityUsed[n] = true;
      console.log("cityused", cityUsed);
      console.log("cityname", this.cityname);

      this.SetButton(citycnt);

      this.UpdateData();
      this.DrawMap();
      this.DrawRoadMap();

      this.alreadyConfirm = true;

      citycnt++;
      nowcitycnt++;
      // console.log(typeof(this.city_po));
    },

    GetName(n) {
      if (n == 1) return "A";
      if (n == 2) return "B";
      if (n == 3) return "C";
      if (n == 4) return "D";
      if (n == 5) return "E";
      if (n == 6) return "F";
      if (n == 7) return "G";
      if (n == 8) return "H";
      if (n == 9) return "I";
      if (n == 10) return "J";
    },

    GetID(n) {
      console.log("n", n);
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
    },

    GetNum(n) {
      if (n == "ci1") return 1;
      if (n == "ci2") return 2;
      if (n == "ci3") return 3;
      if (n == "ci4") return 4;
      if (n == "ci5") return 5;
      if (n == "ci6") return 6;
      if (n == "ci7") return 7;
      if (n == "ci8") return 8;
      if (n == "ci9") return 9;
      if (n == "ci10") return 10;
    },

    GetCode(n) {
      if (n == "ci1") return "A";
      if (n == "ci2") return "B";
      if (n == "ci3") return "C";
      if (n == "ci4") return "D";
      if (n == "ci5") return "E";
      if (n == "ci6") return "F";
      if (n == "ci7") return "G";
      if (n == "ci8") return "H";
      if (n == "ci9") return "I";
      if (n == "ci10") return "J";
    },

    GetCityNum(n) {
      if (n == "A") return 0;
      if (n == "B") return 1;
      if (n == "C") return 2;
      if (n == "D") return 3;
      if (n == "E") return 4;
      if (n == "F") return 5;
      if (n == "G") return 6;
      if (n == "H") return 7;
      if (n == "I") return 8;
      if (n == "J") return 9;
    },

    SetButton(n) {
      if (n == 1) this.isdisabled1 = true;
      if (n == 2) this.isdisabled2 = true;
      if (n == 3) this.isdisabled3 = true;
      if (n == 4) this.isdisabled4 = true;
      if (n == 5) this.isdisabled5 = true;
      if (n == 6) this.isdisabled6 = true;
      if (n == 7) this.isdisabled7 = true;
      if (n == 8) this.isdisabled8 = true;
      if (n == 9) this.isdisabled9 = true;
      if (n == 10) this.isdisabled10 = true;
    },

    SetButtonToFalse(n) {
      if (n == 1) this.isdisabled1 = false;
      if (n == 2) this.isdisabled2 = false;
      if (n == 3) this.isdisabled3 = false;
      if (n == 4) this.isdisabled4 = false;
      if (n == 5) this.isdisabled5 = false;
      if (n == 6) this.isdisabled6 = false;
      if (n == 7) this.isdisabled7 = false;
      if (n == 8) this.isdisabled8 = false;
      if (n == 9) this.isdisabled9 = false;
      if (n == 10) this.isdisabled10 = false;
    },

    toMapModel() {
      this.$router.push({
        path: "/settingMap",
        query: {
          params: JSON.stringify({
            userId: this.userId,
            caseName: 999,
          }),
        },
      });
    },

    correctCity() {
      if (this.alreadyConfirm == false) {
        var n = this.GetUnused();
        var c = "ci" + n;
        console.log(c);
        var ci = document.getElementById(c);
        ci.style.left = 10000 + "px";
        ci.style.top = 10000 + "px";
        this.alreadyConfirm = true;
      }
    },

    changePosition(e) {
      var cinf = "cityinf" + citycnt;
      var ci = document.getElementById(cinf);
      var c = document.getElementById(e);

      ci.style.marginTop = -150 + "px";
      ci.style.marginLeft = 60 + "px";

      var ct = c.style.top;
      var tct = parseInt(ct.substring(0, ct.length - 2));
      console.log("tct", tct);
      if (tct < 150) {
        console.log("你的top不对劲");
        ci.style.marginTop = -tct + "px";
      }
    },

    GetUnused() {
      for (var i = 1; i <= 10; i++) {
        console.log("cityused", cityUsed[i]);
        if (cityUsed[i] == false) {
          return i;
        }
      }
      return 99;
    },

    UpdateData() {
      this.cityname = [];
      this.citypeople = [];
      this.cityInf = [];
      for (var i = 1; i <= 10; i++) {
        if (cityUsed[i] == true) {
          this.cityname.push(cName[i]);
          this.citypeople.push(cPeople[i]);
          this.cityInf.push(cInf[i]);
        }
      }
    },
  },
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
/* @import "../../assets/layui/css/remixicon.css"; */

body {
  overflow: hidden;
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

.tools-wrapper button {
  display: block;
  width: 150px;
  height: 69px;
  color: #000;
  background-color: rgb(241, 245, 253);
  /* background-color: #bfa; */
  border: 1px solid transparent;
}
/* 
.tools-wrapper span{
  background-color: #bfa;
} */
.tools-wrapper button:hover {
  background-color: skyblue;
}
/* 
.tools-wrapper button:active {
  background-color: yellowgreen;
} */

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
  width: 340px;
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

.city-list .panel {
  margin-left: 10px;
  width: 320px;
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
  height: 200px;
  width: 360px;
  background-color: #fff;
  border: 1px solid rgb(187, 187, 187);
  box-shadow: 2px 2px rgba(0, 0, 0, 0.2);
  margin-top: -5px;
  margin-left: 375px;
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
  display: block;
  position: absolute;
  /* left: 5000px;
  top: 3000px; */
}

.img-list .city .city-infor {
  display: none;
  position: absolute;
  height: 185px;
  width: 190px;
  margin-top: -150px;
  margin-left: 60px;
  border: 1px solid rgb(187, 187, 187);
  background-color: #bfa;
  z-index: 9;
}

.img-list .city img {
  position: absolute;
  height: 75px;
  width: 75px;
  z-index: 8;
}

.img-list .city:hover .city-infor {
  display: block;
  z-index: 9;
}

.city-infor .el-form-item {
  margin-bottom: 15px;
}

.city-infor .set_input {
  border-radius: 10px;
  width: 150px;
  margin-left: 20px;
  margin-top: 10px;
  /* margin-bottom: 10px; */
}

.city-infor .el-button--primary,
.city-infor .el-button--info {
  width: 75px;
  height: 30px;
  margin-top: 10px;
  margin-left: 95px;
}

.line_list {
  position: absolute;
  z-index: 3;
}

.line_list .road_line {
  display: block;
  position: absolute;
  height: 5px;
  background-color: #000;
  /* margin-left: 5000px;
  margin-top: 5000px; */
  z-index: 4;
}
</style>

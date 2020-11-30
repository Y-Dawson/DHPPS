<template>
  <div id="simulation">
    <div class="layui-layout layui-layout-admin">
      <div class="layui-header">
        <div class="layui-logo">LOGO</div>
        <div class="layui-logotext">高传染性疾病预测系统</div>
        <!-- <div class="layui-logo">高传染性疾病预测系统</div> -->
        <!-- 头部区域（可配合layui已有的水平导航） -->
        <ul class="layui-nav layui-layout-right">
          <li class="layui-nav-item theme">
            <i class="layui-icon layui-icon-theme"></i>
            <div class="theme-wrapper"></div>
          </li>

          <li class="layui-nav-item" style="line-height: 40px">
            <a href="javascript:;" style="test-align: center">个人中心</a>
          </li>
          <li class="layui-nav-item" style="line-height: 20px">
            <el-avatar
              shape="circle"
              :size="30"
              :fit="fit"
              :src="url"
            ></el-avatar>
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
              @click="ss = !ss"
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

      <div class="add-wrapper">
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
      </div>

      <ul class="city-list">
        <span class="title">已创建：</span>
        <li>
          <div>
            <span class="little-title">城市列表：</span>
            <li id="city_inf" v-for="city in city_po" :key="city">
              {{ city }}
            </li>
            <!-- <span id="city_inf" v-for="(index,item) in city_po"> -->
            <!-- <span>B：400</span>
            <span>C：100</span>
            <span>D：800</span> -->
          </div>
        </li>
        <li>
          <div>
            <span class="little-title">道路列表：</span>
            <li id="city_inf" v-for="road in road_di" :key="road">
              {{ road }}
            </li>
          </div>
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
          >
            <img src="../../assets/img/city.png" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :disabled="isdisabled1"
                  >确认</el-button
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
          >
            <img src="../../assets/img/city.png" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :disabled="isdisabled2"
                  >确认</el-button
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
          >
            <img src="../../assets/img/city.png" alt="" />
            <div class="city-infor">
              <el-form-item prop="population">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
              </el-form-item>

              <el-form-item prop="beginInfected">
                <el-input
                  v-model="cityForm.beginInfected"
                  placeholder="初始感染人数"
                ></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" :disabled="isdisabled3"
                  >确认</el-button
                >
              </el-form-item>
            </div>
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
      </ul>

      <div class="block">
        <el-slider
          v-model="value1"
          :format-tooltip="formatTooltip"
          :step="5"
          show-stops
        ></el-slider>
      </div>
    </el-form>
  </div>
</template>

<script>
import Global from "../../global_vue";

export default {
  data() {
    return {
      ss: false,
      disable: true,
      value1: 0,

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

      cityForm: {
        // cityName: "",
        population: "",
        beginInfected: "",
        distance: "",
        traffic: "",
        // cityleft: Global.cityleft,
        // citytop: Global.citytop,
        // cityleft: this.$root.cityleft,
        // citytop: this.$root.citytop
        cityleft: Global.cityleft,
        citytop: Global.citytop,
      },
      city_po: [],
      road_di: [],
      road_c1: "",
      road_c2: "",
      ci: ["ci1", "ci2", "ci3"],
      ri: ["line1", "line2", "line3"],
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
  methods: {
    sst(ss) {
      this.ss = false;
      this.$router.push("/setting");
    },
    formatTooltip(val) {
      
      return val / 20;
    },
  },
};
</script>

<style>
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
  display: none;
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

.img-list .city:hover .city-infor {
  display: block;
  z-index: 9999;
}

.city-infor .el-form-item {
  margin-bottom: 15px;
}

.city-infor input.el-input__inner {
  border-radius: 10px;
  width: 150px;
  margin-left: 20px;
  margin-top: 10px;
  /* margin-bottom: 10px; */
}

.city-infor .el-button--primary,
.city-infor .el-button--info {
  display: inline;
  margin-top: 10px;
  margin-left: 100px;
}

.line_list .road_line {
  display: block;
  position: absolute;
  height: 5px;
  background-color: #000;
  /* margin-left: 5000px;
  margin-top: 5000px; */
}

.block {
  position: absolute;
  width: 800px;
  margin-left: 325px;
  margin-top: 550px;
}
</style>
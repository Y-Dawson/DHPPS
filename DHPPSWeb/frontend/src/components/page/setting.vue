<template>
  <div id="setting">
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
            <router-link
              :to="{ path: '/profile', query: { userId: userId } }"
              style="margin-left: 10px; float: left"
              >个人中心</router-link
            >
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
      @click="show"
    ></canvas>

    <el-form ref="cityFormRef" :model="cityForm" :rules="cityFormRule">
      <ul class="tools-wrapper">
        <li>
          <el-form-item class="new-pointer">
            <button
              type="primary"
              v-bind:class="{ active1: np }"
              @click="
                np = !np;
                npt(np);
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
                cpt(cp);
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
                dpt(dp);
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
                drt(dr);
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
                bst(bs);
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
                sct(sc);
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
                mct(mc);
              "
            >
              <i class="layui-icon layui-icon-user"></i>
              <span>我的案例</span>
            </button>
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
            @click="
              connect_city('ci1');
              delete_city('ci1');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor">
              <!-- <el-form-item prop="cityName">
                <el-input
                  v-model="cityForm.cityName"
                  placeholder="城市名"
                ></el-input>
              </el-form-item> -->

              <el-form-item prop="population" class="set_input">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
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
                  @click="city_confirm"
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
              connect_city('ci2');
              delete_city('ci2');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor">
              <!-- <el-form-item prop="cityName">
                <el-input
                  v-model="cityForm.cityName"
                  placeholder="城市名"
                ></el-input>
              </el-form-item> -->

              <el-form-item prop="population" class="set_input">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
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
                  @click="city_confirm"
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
              connect_city('ci3');
              delete_city('ci3');
            "
          >
            <img src="../../assets/layui/images/city.png" alt="" />
            <div class="city-infor">
              <el-form-item prop="population" class="set_input">
                <el-input
                  v-model="cityForm.population"
                  placeholder="城市人口"
                ></el-input>
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
                  @click="city_confirm"
                  :disabled="isdisabled3"
                  >确 认</el-button
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
            @click="delete_road('line1')"
          >
            <!-- <div class="road_inf">
              <el-form-item prop="distance">
                <el-input
                  v-model="cityForm.distance"
                  placeholder="人流量"
                ></el-input>
              </el-form-item>
            </div> -->
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
            @click="delete_road('line2')"
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
            @click="delete_road('line3')"
          ></div>
        </li>
      </ul>
    </el-form>
  </div>
</template>

<script>
import Global from "../../global_vue.js";

var citycnt = 1;
var linecnt = 1;
var concnt = 0;
var cn = 0;

export default {
  data() {
    return {
      userId: "",

      np: false,
      cp: false,
      dp: false,
      dr: false,
      bs: false,
      sc: false,
      mc: false,

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
    console.log("案例名：", this.params.casename);
    console.log("类型：", typeof this.params.casename);
    console.log("城市数目：", this.params.citynum);
    console.log("道路数目：", this.params.roadnum);
    console.log("初始城市信息：", this.params.Initcitydata);
    console.log("道路信息：", this.params.Initroaddata);
    console.log("城市坐标：", this.params.Cityposition);
    this.userId = this.params.userId;

    if (this.params.casename != 999) {
      console.log("从模拟界面返回");
      citycnt = this.params.citynum + 1;
      linecnt = 1;
      var cnt = 0;
      for (var j in this.params.Cityposition) {
        var te = this.params.Cityposition[j].split(",");
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
        cid = this.getID(ci);
        var cityentity = document.getElementById(cid);
        cityentity.style.left = x + "px";
        cityentity.style.top = y + "px";
        var nu = this.getNum(cid);
        nu = parseInt(nu);
        this.setButton(nu);
      }

      for (var j in this.params.Initroaddata) {
        console.log(this.params.Initroaddata[j]);
        var ri = this.params.Initroaddata[j].split(",");
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
        var cid1 = this.getID(city1);
        var cid2 = this.getID(city2);
        console.log(cid1, cid2);

        this.drawline(cid1, cid2);
      }

      for (var j in this.params.Initcitydata) {
        var ci = this.params.Initcitydata[j].split(",");
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
      }
    }
  },

  methods: {
    npt(np) {
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

    cpt(cp) {
      console.log("点了");
      this.np = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    dpt(dp) {
      console.log("可以删除节点了");
      this.np = false;
      this.cp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    drt(dr) {
      console.log("可以删除边了");
      this.np = false;
      this.cp = false;
      this.dp = false;
      this.bs = false;
      this.sc = false;
      this.mc = false;
    },

    bst(bs) {
      console.log("开始模拟");
      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.sc = false;
      this.mc = false;

      this.begin_simulation().then((response) => {});
    },

    sct(sc) {
      console.log("保存案例");

      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.mc = false;

      this.save_confirm().then((response) => {});
    },

    mct(mc) {
      console.log("我的案例");
      this.np = false;
      this.cp = false;
      this.dp = false;
      this.dr = false;
      this.bs = false;
      this.sc = false;
      this.$router.push("/caseView");
    },
    // canvas() {
    //   var canvas = this.$refs.canvas;
    //   if (!canvas) {
    //     return false;
    //   } else {
    //     var context = canvas.getContext("2d");
    //     var width = canvas.width;
    //     var height = canvas.height;
    //     var bgimg = document.getElementById("testing");
    //     bgimg.style.width = width;
    //     bgimg.style.height = height;
    //     // var pattern=context.create
    //     addEventListener("click", function (event) {
    //       getMousePos(canvas, event);
    //     });
    //   }
    // },
    // getMousePos(canvas, event) {
    //   var rect = canvas.getBoundingClientRect();
    //   Global.cityleft = event.clientX - rect.left * (canvas.width / rect.width);
    //   Global.cityForm.citytop =
    //     event.clientY - rect.top * (canvas.height / rect.height);
    //   console.log(
    //     "cityleft:" +
    //       Global.cityForm.cityleft +
    //       ", citytop:" +
    //       Global.cityForm.citytop
    //   );
    // },
    drawline(ci1, ci2) {
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
      if (
        (ttcx1 <= ttcx2 && ttcy1 <= ttcy2) ||
        (ttcx1 >= ttcx2 && ttcy1 >= ttcy2)
      ) {
        rotang = Math.asin(parseFloat(dy / dis));
        rotang = (rotang / Math.PI) * 180;
      }
      if (
        (ttcx1 <= ttcx2 && ttcy1 >= ttcy2) ||
        (ttcx1 >= ttcx2 && ttcy1 <= ttcy2)
      ) {
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

    add_day(casename) {
      this.$prompt("请输入模拟天数", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "模拟天数格式不正确",
      })
        .then(({ value }) => {
          this.sc = false;

          var myFormData = new FormData();

          myFormData.append("userid", 3);

          myFormData.append("casename", casename);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var loopcnt = 0;
          var citycnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt == 1) {
              cn = this.city_po[cid].substring(0, 1);
              initpop = this.city_po[cid].substring(7);
            }
            if (loopcnt == 2) {
              initinfect = this.city_po[cid].substring(7);
              citycnt += 1;
              var s =
                "cityname:" +
                cn +
                ",initpop:" +
                initpop +
                ",initinfect:" +
                initinfect;
              city_infor.push(s);
              loopcnt = 0;
            }
          }
          myFormData.append("citynum", citycnt);

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

          myFormData.append("Initcitydata", city_infor);
          myFormData.append("Initroaddata", road_inf);

          var city_position = [];
          loopcnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt % 2 == 1) {
              var cityName = this.city_po[cid].substring(0, 1);
              var cityID = this.getID(cityName);

              console.log("cityName:" + cityName + " cityID:" + cityID);

              var c = document.getElementById(cityID);
              var x = c.style.left.substring(0, c.style.left.length - 2);
              var y = c.style.top.substring(0, c.style.top.length - 2);
              var s = "cityname:" + cityName + ",x:" + x + ",y:" + y;
              city_position.push(s);
            }
          }
          myFormData.append("Cityposition", city_position);

          myFormData.append("daynum", value);

          for (var value of myFormData.values()) {
            console.log(value);
          }

          axios
            .post("http://127.0.0.1:8000/backend/startSimulate/", myFormData)
            .then((response) => {
              alert(JSON.stringify(response));
              alert("保存案例");
              this.$router.push({
                path: "/simulation",
                query: {
                  params: JSON.stringify({
                    userid: 1,
                    casename: casename,
                    citynum: citycnt,
                    roadnum: roadcnt,
                    Initcitydata: city_infor,
                    Initroaddata: road_inf,
                    Cityposition: city_position,
                    Daynum: value,
                    DailyInfected: response,
                  }),
                },
              });
            })
            .catch(function (error) {
              alert(JSON.stringify(response));
              alert("发送失败");
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
      this.$prompt("请输入案例名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "案例名称格式不正确",
      })
        .then(({ value }) => {
          this.add_day(value).then((response) => {});
        })
        .catch(() => {
          this.sc = false;
          this.$message({
            type: "info",
            message: "取消输入",
          });
        });
    },

    save_confirm() {
      this.$prompt("请输入此案例名称", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "案例名称格式不正确",
      })
        .then(({ value }) => {
          this.sc = false;

          var myFormData = new FormData();

          myFormData.append("userid", 3);

          myFormData.append("casename", value);

          var city_infor = [];
          var cn = "Z";
          var initpop = 0;
          var initinfect = 0;
          var loopcnt = 0;
          var citycnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt == 1) {
              cn = this.city_po[cid].substring(0, 1);
              initpop = this.city_po[cid].substring(7);
            }
            if (loopcnt == 2) {
              initinfect = this.city_po[cid].substring(7);
              citycnt += 1;
              var s =
                "cityname:" +
                cn +
                ",initpop:" +
                initpop +
                ",initinfect:" +
                initinfect;
              city_infor.push(s);
              loopcnt = 0;
            }
          }
          myFormData.append("citynum", citycnt);

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

          myFormData.append("Initcitydata", city_infor);
          myFormData.append("Initroaddata", road_inf);

          var city_position = [];
          loopcnt = 0;
          for (var cid in this.city_po) {
            loopcnt += 1;
            if (loopcnt % 2 == 1) {
              var cityName = this.city_po[cid].substring(0, 1);
              var cityID = this.getID(cityName);

              console.log("cityName:" + cityName + " cityID:" + cityID);

              var c = document.getElementById(cityID);
              var x = c.style.left.substring(0, c.style.left.length - 2);
              var y = c.style.top.substring(0, c.style.top.length - 2);
              var s = "cityname:" + cityName + ",x:" + x + ",y:" + y;
              city_position.push(s);
            }
          }
          myFormData.append("Cityposition", city_position);

          for (var value of myFormData.values()) {
            console.log(value);
          }

          axios
            .post("http://127.0.0.1:8000/backend/saveCase/", myFormData)
            .then((response) => {
              alert(JSON.stringify(response));
              alert("保存案例");
            })
            .catch(function (error) {
              alert(JSON.stringify(response));
              alert("发送失败");
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

    show(e) {
      window.cityleft = e.pageX;
      window.citytop = e.pageY;
      // Global.cityleft = e.pageX;
      // Global.citytop = e.pageY;
      this.$set(Global, cityleft, e.pageX);
      this.$set(Global, citytop, e.pageY);
      if (this.np == true) {
        var c = "ci" + citycnt;
        console.log(c);
        var ci = document.getElementById(c);
        var cl = e.pageX - 50;
        var ct = e.pageY - 50;
        ci.style.left = cl + "px";
        ci.style.top = ct + "px";
      }
      if (this.cp == true && concnt == 2) {
        console.log("concnt：" + concnt);

        var mc = document.getElementById("myCanvas");
        var mctx = mc.getContext("2d");

        mctx.moveTo(this.cityx1, this.cityy1);
        mctx.lineTo(this.cityx2, this.cityy2);

        mctx.beginPath();
        mctx.stroke();
        // this.cp = false;
        concnt = 0;
      }
      this.set(data.cityForm, "cityleft", e.pageX + "px");
      this.set(data.cityForm, "citytop", e.pageY + "px");
      this.cityForm.showCity = true;
      console.log(
        "cityleft:" + Global.cityleft + ", citytop:" + Global.citytop
      );
      console.log("cityleft:" + this.cityleft + ", citytop:" + this.citytop);
    },

    road_confirm(tcx1, tcy1, tcx2, tcy2, dx, dy, dis) {
      var tra = 0;
      this.$prompt("请输入此路人流量", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        inputPattern: /^[0-9]/,
        inputErrorMessage: "人流量格式不正确",
      })
        .then(({ value }) => {
          var road_inf = this.road_c1 + "-" + this.road_c2 + ":" + value;
          console.log(road_inf);

          console.log("tcx1：" + tcx1);

          var ttcx1 = parseInt(tcx1);
          var ttcx2 = parseInt(tcx2);
          var ttcy1 = parseInt(tcy1);
          var ttcy2 = parseInt(tcy2);

          var rotang = 0;
          if (
            (ttcx1 <= ttcx2 && ttcy1 <= ttcy2) ||
            (ttcx1 >= ttcx2 && ttcy1 >= ttcy2)
          ) {
            rotang = Math.asin(parseFloat(dy / dis));
            rotang = (rotang / Math.PI) * 180;
          }
          if (
            (ttcx1 <= ttcx2 && ttcy1 >= ttcy2) ||
            (ttcx1 >= ttcx2 && ttcy1 <= ttcy2)
          ) {
            rotang = Math.asin(parseFloat(dy / dis));
            rotang = (rotang / Math.PI) * 180;
            rotang = 180 - rotang;
          }

          var ll = document.getElementById("line" + linecnt);

          ll.style.left = (ttcx1 + ttcx2) / 2 - parseInt(dis) / 2 + 20 + "px";
          ll.style.top = (ttcy1 + ttcy2) / 2 + 50 + "px";
          ll.style.width = parseInt(dis) + "px";
          ll.style.transform = "rotate(" + rotang + "deg)";

          console.log("dis_cos：" + (parseInt(dis) * Math.cos(rotang)) / 2);
          console.log("ll.style.left：" + ll.style.left);
          console.log("ttcx1：" + ttcx1);

          console.log("dis：" + dis);
          console.log("width：" + ll.style.width);

          this.road_di.push(road_inf);

          linecnt += 1;
          this.cp = false;
          concnt = 0;
        })
        .catch(() => {
          this.cp = false;
          concnt = 0;
          this.$message({
            type: "info",
            message: "取消输入",
          });
          tra = -1;
        });
      console.log(tra);
      return tra;
    },

    connect_city(e) {
      if (this.cp == true) {
        console.log(e);
        concnt += 1;
        var c = document.getElementById(e);
        console.log("left：" + c.style.left + " top：" + c.style.top);
        // console.log(this.cityForm.cityName);
        if (concnt == 1) {
          this.cityx1 = c.style.left;
          this.cityy1 = c.style.top;
          for (var k in this.ci) {
            var k1 = parseInt(k);
            var tc = document.getElementById(this.ci[k1]);
            if (tc.style.left == c.style.left && tc.style.top == c.style.top) {
              this.road_c1 = this.getName(k1 + 1);
              break;
            }
          }
          // this.road_c1 = c.cityForm.cityName;
          console.log(this.road_c1);
        }
        if (concnt == 2) {
          console.log("第二次了");

          this.cityx2 = c.style.left;
          this.cityy2 = c.style.top;

          console.log("cityx1:" + this.cityx1 + ", cityy1:" + this.cityy1);
          console.log("cityx2:" + this.cityx2 + ", cityy2:" + this.cityy2);

          for (var k in this.ci) {
            var k1 = parseInt(k);
            var tc = document.getElementById(this.ci[k1]);
            if (tc.style.left == c.style.left && tc.style.top == c.style.top) {
              this.road_c2 = this.getName(k1 + 1);
              break;
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
          this.road_confirm(
            tcx1,
            tcy1,
            tcx2,
            tcy2,
            dx,
            dy,
            dis
          ).then((response) => {});
        }
      }
    },

    confirm_delete_city(e) {
      this.$confirm("此操作将删除该城市及其相邻的道路, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          var c = document.getElementById(e);

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
          this.city_po.splice(cn*2, 2);

          for (var i in this.city_po) {
            console.log(this.city_po[i]);
          }

          var city_no = e.substring(2, 3);
          var city_tno = parseInt(city_no);
          console.log("city：" + e);
          var ce = this.getName(city_tno);
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
              cid = this.getID(c2);
              // this.road_di.splice(j, 1);
              wait_delete.push(j);
            }
            if (c2 == ce) {
              cid = this.getID(c1);
              wait_delete.push(j);
              // this.road_di.splice(j, 1);
            }
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
              var tr = document.getElementById(this.ri[k]);
              var td = parseInt(dis);
              var wi = tr.style.width;
              var tw = wi.substring(0, wi.length - 2);
              var ttw = parseInt(tw);
              console.log("dis：" + td + " width：" + ttw);
              if (td == ttw) {
                tr.style.left = 10000 + "px";
                tr.style.top = 10000 + "px";
                break;
              }
            }
          }

          var twd = wait_delete.reverse();
          for (var j in twd) {
            this.road_di.splice(twd[j], 1);
          }

          c.style.left = 10000 + "px";
          c.style.top = 10000 + "px";
          this.dp = false;
          this.$message({
            type: "success",
            message: "删除成功!",
          });
        })
        .catch(() => {
          this.dp = false;
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },

    delete_city(e) {
      if (this.dp == true) {
        this.confirm_delete_city(e).then((response) => {});
      }
    },

    delete_road(e) {
      if (this.dr == true) {
        var r = document.getElementById(e);
        for (var j in this.road_di) {
          var c1 = this.road_di[j].substring(0, 1);
          var c2 = this.road_di[j].substring(2, 3);
          var cid1 = this.getID(c1);
          var cid2 = this.getID(c2);
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
            break;
          }
        }
        r.style.left = 10000 + "px";
        r.style.top = 10000 + "px";
        this.dr = false;
      }
    },

    // changeString(str) {
    //   return str.replace(/<br>/g, "\n");
    // },

    city_confirm() {
      this.np = false;
      // console.log("city_Name:" + this.cityForm.cityName);
      console.log("city_population:" + this.cityForm.population);
      console.log("city_Infected:" + this.cityForm.beginInfected);
      var cn = this.getName(citycnt);

      var cy = cn + ": 总人口:" + this.cityForm.population;
      this.city_po.push(cy);
      cy = "初始感染人数:" + this.cityForm.beginInfected;
      this.city_po.push(cy);

      this.setButton(citycnt);

      citycnt++;
      this.disable = false;
      // console.log(typeof(this.city_po));
    },

    getName(n) {
      if (n == 1) return "A";
      if (n == 2) return "B";
      if (n == 3) return "C";
      if (n == 4) return "D";
      if (n == 5) return "E";
      if (n == 6) return "F";
      if (n == 7) return "G";
    },

    getID(n) {
      if (n == "A") return "ci1";
      if (n == "B") return "ci2";
      if (n == "C") return "ci3";
      if (n == "D") return "ci4";
    },

    getNum(n) {
      if (n == "ci1") return 1;
      if (n == "ci2") return 2;
      if (n == "ci3") return 3;
      if (n == "ci4") return 4;
    },

    setButton(n) {
      if (n == 1) this.isdisabled1 = true;
      if (n == 2) this.isdisabled2 = true;
      if (n == 3) this.isdisabled3 = true;
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
  background-color: #bfa;
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

.line_list .road_line {
  display: block;
  position: absolute;
  height: 5px;
  background-color: #000;
  /* margin-left: 5000px;
  margin-top: 5000px; */
}
</style>
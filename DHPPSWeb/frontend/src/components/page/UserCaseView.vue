<template>
  <div id="app">
    <div class="layui-layout layui-layout-admin">
      <topBar layoutName='个人中心' :userId="userId"></topBar>
      <div class="layui-side layui-bg-black">
        <div class="layui-side-scroll">
          <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
          <ul class="layui-nav layui-nav-tree" lay-filter="test">
            <li class="layui-nav-item layui-nav-itemed">
              <div
                style="
                  text-align: center;
                  background-color: #fff;
                  font-size: 16px;
                  color: rgb(132, 132, 136);">
                <i class="layui-icon layui-icon-app" style="font-size: 20px; color: rgb(173, 173, 173)"></i>
                系统菜单
              </div>
              <dl class="layui-nav-child">
                <dd>
                  <router-link :to="{ path: '/profile', query: { userId: userId } }">个人资料</router-link>
                </dd>
                <dd>
                  <router-link :to="{ path: '/modifyPI', query: { userId: userId } }">修改资料</router-link>
                </dd>
              </dl>
              <router-link :to="{ path: '/caseView', query: { userId: userId } }">案例查看</router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="layui-body">
        <!-- 内容主体区域 -->
        <div style="padding: 15px">
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <ul class="layui-tab-title">
              <li class="layui-this" style="color: #55587e">案例查看</li>
            </ul>
            <div class="layui-tab-content">
              <div class="box" style="text-align: center">
                <div
                  class="box-card-group"
                  style="
                    margin-left: 60px;
                    margin-top: 20px;
                    width: auto;
                    height: 450px;
                    text-align: left;
                  "
                >
                  <el-col
                    :span="7"
                    v-for="(item, index) in currentPageData.data"
                    :key="index"
                  >
                    <el-card class="box-card">
                      <div slot="header" class="clearfix">
                        <i
                          class="layui-icon layui-icon-template-1"
                          style="
                            margin-right: 10px;
                            font-size: 40px;
                            color: rgb(173, 173, 173);
                          "
                        ></i>
                        <span id="returnContent">{{ item.casename }}</span>
                        <div
                          style="
                            font-size: 8px;
                            line-height: 20px;
                            float: right;
                            text-align: right;
                          "
                        >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: #55587e"
                            @click="Edit(item.caseid)"
                            >进入编辑</el-button
                          >
                          <el-button
                            id="delete"
                            type="text"
                            style="font-size: 8px; color: rgb(221, 0, 0)"
                            @click="Open(item.caseid)"
                            >删除</el-button
                          >
                        </div>
                      </div>
                      <dl class="box-text">
                        <span>初始城市数量：</span>
                        <span id="returnContent">{{ item.citynumber }}</span>
                        <br />
                        <span>初始道路数量：</span>
                        <span id="returnContent">{{ item.roadnumber }}</span>
                        <br />
                        <span>初始总人口：</span>
                        <span id="returnContent">{{ item.inittotal }}</span>
                        <br />
                        <span>初始感染人口：</span>
                        <span id="returnContent">{{
                          item.inittotalinfected
                        }}</span>
                      </dl>
                    </el-card>
                  </el-col>
                </div>
                <div class="paginate">
                  <button class="primaryb" @click="GetPrevPage()">上一页</button>
                  <span>第{{ currentPage }}页/共{{ totalPage }}页</span>
                  <button class="primaryb" @click="GetNextPage()">下一页</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import topBar from '../common/topBar.vue';
export default {
  name: "caseView",
  inject: ["reload"],
  components:{
      topBar
    },
  data: function () {
    return {
      cases: [],
      content: [],
      userId: this.$route.query.userId,
      contentList: [],
      isBackground: true,
      casenum: 8,
      test: 0,
      // 头像
      fits: ["fill"],
      url: "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 6, // 每页显示数量
      currentPageData: [], //当前页显示内容
    };
  },
  created: function () {
    this.GetContent(this.userId);
  },
  mounted: function () {
    this.GetCaseContent();
    this.SetPages();
  },
  methods: {
    //上一页
    GetPrevPage() {
      if (this.currentPage == 1) return;
      this.currentPage--;
      this.GetCaseContent();
    },
    // 下一页
    GetNextPage() {
      if (this.currentPage == this.totalPage) return;
      this.currentPage++;
      this.GetCaseContent();
    },
    SetPages() {
      if (this.totalPage < 1) totalPage = 1;
    },
    GetContent: function (userId) {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/profile/" + userId + "/")
        .then((response) => (self.content = response.data))
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    //获取案例内容
    GetCaseContent: function () {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/case/", {
          params: {
            userid: this.$route.query.userId,
            pageSize: 6,
            page: self.currentPage,
          },
        })
        .then(
          (response) => (
            (self.currentPageData = response.data),
            (self.totalPage = Math.ceil(
              self.currentPageData.pagination / self.pageSize
            ))
          )
        )
        .catch(function (error) {
          // 请求失败处理
          alert('数据请求失败')
        });
    },
    // 案例编辑
    Edit: function (id) {
      var self = this;
      let data = new FormData();
      data.append("caseid", id);
      axios
        .post("http://127.0.0.1:8000/backend/getCaseInfo/", data)
        .then((response) => {
          self.cases = response.data.cases;
          console.log(JSON.stringify(self.cases));

          console.log(self.cases.Initcitydata);
          var city_inf = [];
          for (var j in self.cases.Initcitydata) {
            var s =
              "cityname:" +
              self.cases.Initcitydata[j].cityname +
              ",initpop:" +
              self.cases.Initcitydata[j].initpop +
              ",initinfect:" +
              self.cases.Initcitydata[j].initinfect;
            console.log("s:", s);
            city_inf.push(s);
          }

          var road_inf = [];
          for (var j in self.cases.Initroaddata) {
            var s =
              "departure:" +
              self.cases.Initroaddata[j].departure +
              ",destination:" +
              self.cases.Initroaddata[j].destination +
              ",volume:" +
              self.cases.Initroaddata[j].volume;
            console.log("s:", s);
            road_inf.push(s);
          }

          var city_pos = [];
          for (var j in self.cases.Cityposition) {
            var s =
              "cityname:" +
              self.cases.Cityposition[j].cityname +
              ",x:" +
              self.cases.Cityposition[j].x +
              ",y:" +
              self.cases.Cityposition[j].y;
            console.log("s:", s);
            city_pos.push(s);
          }

          this.$router.push({
            path: "/setting",
            query: {
              params: JSON.stringify({
                userId: this.userId,
                casename: this.cases.casename,
                citynum: this.cases.citynum,
                roadnum: this.cases.roadnum,
                Initcitydata: city_inf,
                Initroaddata: road_inf,
                Cityposition: city_pos,
              }),
            },
          });
        })
        .catch(function (error) {
          alert(JSON.stringify(error.response));
          alert("数据请求失败wdnmd");
        });
    },
    DeleteCaseContent: function (id) {
      var self = this;
      axios
        .delete("http://127.0.0.1:8000/backend/case/" + id, {})
        .then(
          (response) => (self.currentPageData = response.data)
        )
        .catch(function (error) {
          alert('数据请求失败')
        });
    },
    Open(id) {
      this.$confirm("此操作将永久删除该文件, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.DeleteCaseContent(id),
            this.GetCaseContent(),
            this.reload(),
            this.$message({
              type: "success",
              message: "删除成功!",
            });
          this.GetCaseContent();
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
  },
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
.list {
  text-align: center;
  margin: 10px 300px;
}
.paginate {
  margin-top: 20px;
  margin-left: -70px;
}
.primaryb {
  border: 0px;
  box-shadow: 3px 3px 5px #d6d6d6;
  background: #ffffff;
  width: 80px;
  height: 30px;
}
.primaryb:hover {
  background: #8b9bbd;
}
/* 表单 */
.el-form {
  text-align: center;
}
.el-form-item {
  margin-top: 20px;
  width: 320px;
}
/* 案例块文字内容 */
.box-text {
  margin-left: 5px;
  line-height: 18px;
  font-size: 12px;
  color: rgb(71, 71, 71);
}
/* 案例块样式 */
.box-card {
  width: 240px;
  float: left;
  margin-right: 50px;
  margin-bottom: 20px;
}
.reset {
  background: #fff;
  border: 1px #55587e solid;
}
.el-checkbox :hover {
  background: #8b9bbd;
}

/* 左侧导航栏 */
/* 第一个hover */
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
  font-size: 10px;
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
  font-size: 10px;
}
.layui-layout-admin .layui-header {
  background-color: #8b9bbd;
}
.layui-side-scroll {
  position: relative;
  width: 220px;
  height: 100%;
  overflow-x: hidden;
  background-color: #ffffff;
}
/* 选项卡 */
.layui-tab-brief {
  color: #61637c;
}
.layui-tab-title {
  color: #61637c;
}
.layui-tab-brief > .layui-tab-more li.layui-this:after,
.layui-tab-brief > .layui-tab-title .layui-this:after {
  border: none;
  border-radius: 0;
  border-bottom: 2px solid rgb(245, 152, 65);
}
.layui-this {
  color: #55587e;
  font-weight: bold;
}
.layui-form-label {
  text-align: left;
  width: 45px;
}
/* 按钮 */
.layui-btn {
  background-color: #55587e;
}
.layui-btn-primary {
  background-color: #fff;
}
</style>

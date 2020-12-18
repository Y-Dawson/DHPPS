<template>
  <div id="app">
    <div class="layui-layout layui-layout-admin">
      <!-- 导航栏 -->
      <TopBar layoutName="后台管理系统" :BaruserId="BaruserId"></TopBar>
      <div class="layui-side layui-bg-black">
        <div class="layui-side-scroll">
          <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
          <ul class="layui-nav layui-nav-tree" lay-filter="test">
            <li class="layui-nav-item layui-nav-itemed">
              <div style="text-align: center;background-color: #fff;font-size: 16px;color: rgb(132, 132, 136);">
                <i class="layui-icon layui-icon-app" style="font-size: 20px; color: rgb(173, 173, 173)"></i>
                系统菜单
              </div>
              <a class="" href="javascript:;">信息管理</a>
              <dl class="layui-nav-child">
                <dd>
                  <router-link :to="{ path: '/SuperCaseManage', query: { BaruserId: this.BaruserId } }">
                    案例管理
                  </router-link>
                </dd>
                <dd>
                  <router-link :to="{ path: '/SuperModelView', query: { BaruserId: this.BaruserId } }">
                    模型查看
                  </router-link>
                </dd>
              </dl>
            </li>
          </ul>
        </div>
      </div>

      <div class="layui-body">
        <!-- 内容主体区域 -->
        <div style="padding: 15px">
          <!-- 选项卡 -->
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <ul class="layui-tab-title">
              <li class="layui-off">
                <router-link :to="{ path: '/SuperUserManage', query: { BaruserId: this.BaruserId } }">
                  用户管理
                </router-link>
              </li>
              <li class="layui-off">
                <router-link :to="{ path: '/SuperStaffManage', query: { BaruserId: this.BaruserId } }">
                  员工管理
                </router-link>
              </li>
              <li class="layui-this" style="color: #55587e">编辑</li>
            </ul>
            <div class="layui-tab-content">
              <!-- 编辑部分 -->
              <ul style="margin: 0px 50px; font-size: 14px">
                <li style="margin-top: 20px">
                  <div class="userName">用户名称：{{ EditName }}</div>
                </li>
                <li style="margin-top: 20px">
                  <div class="userTed">用户手机号：{{ EditTel }}</div>
                </li>
                <li style="margin-top: 20px">
                  <label class="remark">备注：</label>
                  <div style="margin-top: 20px">
                    <textarea
                      id="desc"
                      placeholder="请输入备注内容..."
                      v-model="content"
                      class="layui-textarea"
                      style="width: 500px"
                    ></textarea>
                  </div>
                  <!-- <div>{{desc}}</div> -->
                  <div style="margin-top: 20px">
                    <button type="submit" @click="RemarkIsEmpty(userId)">
                      立即提交
                    </button>
                    <button type="reset" @click="RemarkEmpty">重置</button>
                  </div>
                </li>
                <li style="margin-top: 20px">
                  <label class="authority">更改权限设置： </label>
                  <select id="selected" v-model="selected" name="authority">
                    <option value="普通用户">普通用户</option>
                    <option value="管理员">管理员</option>
                  </select>
                  <button @click="AuthorityIsEmpty(userId)">确定</button>
                  <!-- </div> -->
                </li>
              </ul>
            </div>
          </div>

          <div class="layui-footer">
            <!-- 底部固定区域 -->
            © layui.com - 底部固定区域
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script src="layui.js"></script>

<script>
  import TopBar from "../common/TopBar.vue";
  export default {
    name: "SuperEdit",
    components: {
      TopBar,
    },
    data() {
      return {
        BaruserId: this.$route.query.BaruserId,
        EditTel: this.$route.query.uT,
        EditName: this.$route.query.uN,
        userId: this.$route.query.uI,
        UserCreate: this.$route.query.uC,
      };
    },
    methods: {
      RemarkEmpty() {
        $("#desc").val("");
      },
      RemarkIsEmpty(Id) {
        if ($("#desc").val() == "") this.$message("请输入备注信息");
        else this.PutRemark(Id);
      },
      PutRemark(Id) {
        var self = this;
        axios
          .put("http://127.0.0.1:8000/backend/accountInfo/" + Id + "/", {
            remark: $("#desc").val(),
          })
          .then(
            (response) => (
              (self.content = response), this.$message("修改备注成功")
            )
          )
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
      },
      AuthorityIsEmpty(Id) {
        if (
          $("#selected").val() == "管理员" ||
          $("#selected").val() == "普通用户"
        )
          this.PutAuthority(Id);
        else this.$message("请选择权限");
      },
      PutAuthority(Id) {
        var self = this;
        axios
          .put("http://127.0.0.1:8000/backend/accountInfo/" + Id + "/", {
            authority: $("#selected").val(),
            themeNo: 1,
          })
          .then(
            (response) => (
              (self.content = response), this.$message("修改权限成功")
              // alert(JSON.stringify(response))
            )
          )
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
      },
    },
  };
</script>

<style scoped>
  @import "../../assets/layui/css/layui.css";
  /* 左侧导航栏 */
  /* 第一个hover */
  .layui-nav-tree .layui-nav-item a {
    text-align: center;
    font-weight: bold;
    background-color: rgb(131, 137, 158);
  }
  .layui-nav-tree .layui-nav-item a:hover {
    background-color: #55587e;
  }
  /* 第二三块的字体 */
  .layui-nav-tree .layui-nav-child a {
    text-align: center;
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
  /* 左侧位置 */
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
</style>

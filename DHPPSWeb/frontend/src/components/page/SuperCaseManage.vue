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
              <div
                style="
                  text-align: center;
                  background-color: #fff;
                  font-size: 16px;
                  color: rgb(132, 132, 136);
                "
              >
                <i
                  class="layui-icon layui-icon-app"
                  style="font-size: 20px; color: rgb(173, 173, 173)"
                ></i>
                系统菜单
              </div>
              <dl class="layui-nav-child">
                <dd>
                  <router-link
                    :to="{ path: '/SuperUserManage', query: { BaruserId: this.BaruserId } }"
                    >信息管理</router-link
                  >
                </dd>
              </dl>
              <a class="" href="javascript:;">案例管理</a>
              <dl class="layui-nav-child">
                <dd>
                  <router-link
                    :to="{ path: '/SuperModelView', query: { BaruserId: this.BaruserId } }"
                    >模型查看</router-link
                  >
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
              <li class="layui-this" style="color: #55587e">案例管理</li>
              <li class="layui-off">案例参数</li>
            </ul>
          </div>
          <div class="layui-tab-Content">
            <!-- 列表 -->
            <div class="list">
              <table class="layui-table" lay-size="sm" lay-even lay-skin="row">
                <colgroup>
                  <col width="150" />
                  <col width="200" />
                  <col />
                </colgroup>
                <thead>
                  <tr style="text-align: center">
                    <th style="width: 15%; text-align: center">用户ID</th>
                    <th style="width: 15%; text-align: center">用户昵称</th>
                    <th style="width: 15%; text-align: center">案例数量</th>
                    <th
                      style="width: 15%; text-align: center"
                      lay-data="{sort:true}"
                    >
                      创建时间
                    </th>
                    <th style="width: 15%; text-align: center">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in Content" :key="item.userId">
                    <td>{{ item.userId }}</td>
                    <td>{{ item.userName }}</td>
                    <td>{{ item.caseNumber }}</td>
                    <td>{{ item.createDate }}</td>
                    <td>
                      <button class="buttonA">
                        <router-link
                          :to="{
                            path: '/SuperCaseEdit',
                            query: { uI: item.userId, BaruserId: BaruserId },
                          }"
                          >案例编辑</router-link
                        >
                      </button>
                      <button
                        class="buttonA"
                        type="danger"
                        @click="HandleDel(item.userId)"
                      >
                        删 &nbsp;&nbsp; 除
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="paginate">
              <button class="primaryb" @click="PrevPage()">上一页</button>
              <span>第{{ CurrentPage }}页/共{{ TotalPage }}页</span>
              <button class="primaryb" @click="NextPage()">下一页</button>
            </div>
          </div>
        </div>

        <div class="layui-footer">
          <!-- 底部固定区域 -->
          © layui.com - 底部固定区域
        </div>
      </div>
    </div>
  </div>
</template>

<script src="layui.js"></script>
<script>
  import TopBar from "../common/TopBar.vue";
  export default {
    name: "SuperCaseManage",
    components: {
      TopBar,
    },
    data() {
      return {
        BaruserId: this.$route.query.BaruserId,
        //分页
        TotalPage: 3, // 统共页数，默认为1
        CurrentPage: 1, //当前页数 ，默认为1
        PageSize: 6, // 每页显示数量
        Content: [], //当前页显示内容
        Paginate: 10, //当前页显示内容
      };
    },
    created: function () {
      //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
      this.GetContent();
    },
    methods: {
      GetContent: function () {
        var self = this;
        axios
          .get("http://127.0.0.1:8000/backend/userManage/", {
            params: {
              pageSize: 10,
              page: self.CurrentPage,
            },
          })
          .then(
            (response) => (
              (self.Content = response.data.data),
              (self.Paginate = response.data.pagination),
              (self.PageSize = response.data.pageSize),
              (self.TotalPage = Math.ceil(self.Paginate / self.PageSize)),
              this.TestPage()
              // alert(JSON.stringify(response))
            )
          )
          .catch(function (error) {
            // 请求失败处理
            alert("数据请求失败wdnmd");
          });
      },
      HandleDel(id) {
        this.$confirm("确认删除该用户吗？", "系统提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.DeleteContent(id);
            this.$message({
              type: "success",
              message: "删除成功！",
            });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "取消删除！",
            });
          });
      },
      DeleteContent: function (id) {
        var self = this;
        var date = $("#input1").val();
        axios
          .delete("http://127.0.0.1:8000/backend/accountInfo/" + id + "/", {})
          .then(
            (response) => (
              (self.Content = response), self.GetContent()
              // alert(JSON.stringify(response))
            )
          )
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
      },
      //上一页
      PrevPage() {
        if (this.CurrentPage == 1) return;
        this.CurrentPage--;
        this.GetContent();
      },
      // 下一页
      NextPage() {
        if (this.CurrentPage == this.TotalPage) return;
        this.CurrentPage++;
        this.GetContent();
      },
      TestPage: function () {
        if (this.TotalPage == 0) this.TotalPage = 1;
      },
    },
  };
</script>

<style scoped>
  @import "../../assets/layui/css/layui.css";
  /* 列表大小 */
  .list {
    text-align: center;
    margin: 20px 40px;
  }
  /* 分页 */
  .paginate {
    margin-top: 20px;
    text-align: center;
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
  /* 编辑删除按钮 */
  .buttonA {
    border: 5px;
    box-shadow: 3px 3px 5px #d6d6d6;
    width: 60px;
    height: 20px;
  }
  .buttonA:hover {
    background: #8b9bbd;
  }

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
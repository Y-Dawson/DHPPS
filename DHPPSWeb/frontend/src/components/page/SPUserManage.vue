<template>
  <!-- 实现了生日日期选择，没有实现输入框校验！！！ -->
    <div id="app">
        <div class="layui-layout layui-layout-admin">
            <!-- 导航栏 -->
            <topBar layoutName='后台管理系统'></topBar>
            <div class="layui-side layui-bg-black">
                <div class="layui-side-scroll">
                <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
                    <ul class="layui-nav layui-nav-tree"  lay-filter="test">
                        <li class="layui-nav-item layui-nav-itemed">
                            <div style="text-align:center;background-color:#fff;font-size: 16px;color: rgb(132, 132, 136);">
                                <i class="layui-icon layui-icon-app" style="font-size: 20px; color:rgb(173, 173, 173);"></i>
                                系统菜单
                            </div>
                            <a class="" href="javascript:;" >信息管理</a>
                            <dl class="layui-nav-child">
                                <dd><router-link to='/SPCaseManage'>案例管理</router-link></dd>
                                <dd><a href="javascript:;">模型查看</a></dd>
                            </dl>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="layui-body">
                <!-- 内容主体区域 -->
                <div style="padding: 15px;">
                <!-- 选项卡 -->
                    <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
                        <ul class="layui-tab-title">
                            <li class="layui-this" style="color: #55587e;">用户管理</li>
                            <router-link to='/SPStaffManage'><li class="layui-off">员工管理</li></router-link>
                            <li class="layui-off">编辑</li>
                        </ul>
                    <div class="layui-tab-content">
                    <!-- 列表 -->
                        <div class="list">
                            <table class="layui-table" lay-size="sm" lay-even lay-skin="row">
                                <colgroup>
                                    <col width="150">
                                    <col width="200">
                                    <col>
                                </colgroup>
                                <thead>
                                <tr>
                                    <th style="width: 10%;text-align: center;">用户ID</th>
                                    <th style="width: 10%;text-align: center;">用户昵称</th>
                                    <th style="width: 10%;text-align: center;" lay-data="{sort:true}">创建时间</th>
                                    <th style="width: 20%;text-align: center;">手机号</th>
                                    <th style="width: 10%;text-align: center;">案例数量</th>
                                    <th style="width: 10%;text-align: center;">备注</th>
                                    <th style="width: 20%;text-align: center;">操作</th>
                                </tr>
                                </thead>
                            <tbody>
                                <!-- <span>{{ content }}</span> -->
                                <tr v-for="item in content" :key="item.userid">
                                    <td>{{item.userid}}</td>
                                    <td>{{item.username}}</td>
                                    <td>{{item.createdate}}</td>
                                    <td>{{item.phonenumber}}</td>
                                    <td>{{item.casenumber}}</td>
                                    <td>{{item.remark}}</td>
                                    <td>
                                        <button><router-link :to="{path:'/SPEdit',query:{uN:item.username,uT:item.phonenumber,uI:item.userid,uC:item.createdate}}">编辑</router-link></button>
                                        <button type="danger" @click="handleDel(item.userid)">删除</button>
                                    </td>
                                </tr>
                            </tbody>
                            </table>
                            <tfoot>
                                
                            </tfoot>
                        </div>
                    </div>
                    </div>
                    <div class="paginate">
                        <button class="primaryb" @click="prevPage()">
                        上一页
                        </button>
                        <span>第{{currentPage}}页/共{{totalPage}}页</span>
                        <button class="primaryb" @click="nextPage()">
                        下一页
                        </button>
                    </div>
                </div>
            </div>
            <div class="layui-footer">
                <!-- 底部固定区域 -->
                © layui.com - 底部固定区域
            </div>
        </div>
    </div>
</template>
<script src="layui.js"></script>
<script>
import topBar from '../common/topBar.vue';
export default {
    name:'userManagement',
    components:{
      topBar
    },
    data() {
      return {
        //分页
        totalPage: 3, // 统共页数，默认为1
        currentPage: 1, //当前页数 ，默认为1
        pageSize: 4, // 每页显示数量
        content: [], //当前页显示内容
        paginate: 10
      };
    },
    created: function () {
      //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
      this.getContent()
    },
    methods: {
      getContent: function () {
        var self = this;
        axios
          .get("http://127.0.0.1:8000/backend/generalUserManage/",{
            params:{
              pageSize: 10,
              page: self.currentPage
            }
          })
          .then(response => (
            self.content = response.data.data,
            self.paginate=response.data.pagination,
            self.pageSize=response.data.pageSize,
            self.totalPage=Math.ceil(self.paginate / self.pageSize)
            // alert(JSON.stringify(response.data)),
            // alert(self.pageSize)
          ))
          .catch(function (error) { // 请求失败处理
            alert("数据请求失败wdnmd");
          });
      },
      handleDel(id) {
        this.$confirm("确认删除该用户吗？","系统提示",{
          confirmButtonText:"确定",
          cancelButtonText:"取消",
          type:"warning"
        })
          .then(()=>{
            this.deleteContent(id);
            this.$message({
              type:"success",
              message:"删除成功！"
            });
          })
          .catch(()=>{
            this.$message({
              type:"info",
              message:"取消删除！"
            });
          })
      },
      deleteContent: function (id) {
        var self = this;
        // var date = $("#input1").val();
        axios
          .delete('http://127.0.0.1:8000/backend/accountInfo/'+id+'/',{
              
          })
          .then(response => (
            self.content = response,
            self.getContent()
            // alert(JSON.stringify(response))
          ))
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
        },
        //上一页
        prevPage() {
            if (this.currentPage == 1) return;
             this.currentPage--;
             this.getContent();
            
        },
        // 下一页
        nextPage() {
            if (this.currentPage == this.totalPage) return ;
             this.currentPage++;
             this.getContent();
            
        }
    }
  }
</script>

// 修改elementui的样式
<style>
.el-pagination.is-background .el-pager li:not(.disabled).active{
  background-color:#55587e!important;
}
.el-pagination.is-background .el-pager li:not(.disabled).active:hover{
    color:#fff !important;
}
.el-pagination.is-background .el-pager li:hover{
  color:#55587e !important;
}
</style>

<style scoped>
@import "../../assets/layui/css/layui.css";


.list{
  text-align:center;
  margin: 10px 300px;
}
.paginate{
  margin-top: 20px;
  text-align: center;
}
.primaryb{
  border: 0px;
  box-shadow:3px 3px 5px #d6d6d6;
  background: #ffffff;
  width: 80px;
  height: 30px;
}
.primaryb:hover{
  background: #8b9bbd;
}
/* 表单 */
.el-form {
  text-align:center;
}
.el-form-item{
  margin-top: 20px;
  width: 320px;
}
/* 案例块文字内容 */
.box-text{
    margin-left: 5px;
    line-height: 18px;
    font-size: 12px;
    color:rgb(71, 71, 71);
}
/* 案例块样式 */
.box-card{
    width:240px;
    float:left;
    margin-right:50px;
    margin-bottom:20px;
}
/* el按钮 */
.el-button{
  margin-top: 30px;
  background: #55587e;
  border:0px;
  width: 60px;
  height: 30px;
}
.reset{
  background: #fff;
  border:1px #55587e solid;
}
.el-checkbox :hover{
  background: #8b9bbd;
}

/* 左侧导航栏 */
         /* 第一个hover */
        .layui-nav-tree .layui-nav-item a{
            text-align: center;
            font-weight: bold;
            background-color: rgb(131, 137, 158);
        }
        .layui-nav-tree .layui-nav-item a:hover{background-color:#55587e}
        /* 第二三块的字体 */
        .layui-nav-tree .layui-nav-child a{
            text-align: center;
            height:40px;
            line-height:40px;
            font-weight:normal;
            background-color:#fff;
            color:rgba(10, 12, 22, 0.411)
        }
        /* 第二三块的背景 */
        .layui-nav-itemed>.layui-nav-child{
            display:block;
            padding:0;
            background-color:rgba(212, 187, 187, 0.966)
        }
        /* 第二三块的hover */
        .layui-nav .layui-nav-child a:hover{background-color:#55587e;color:rgb(255, 255, 255)}
        /* LOGO */
       .layui-layout-admin .layui-logo{
            position:absolute;
            left:0;
            top:0;
            width:200px;
            height:50%;
            line-height:40px;
            text-align:center;
            color:#ffffff;
        }
        .layui-layout-admin .layui-logotext{
            position:absolute;
            left:0;
            top:0;
            width:200px;
            height:50%;
            line-height:80px;
            text-align:center;
            color:#ffffff;
        }
        .layui-layout-admin .layui-header{background-color:#8b9bbd}
        .layui-side-scroll{
            position:relative;
            width:220px;height:100%;
            overflow-x:hidden;
            background-color: #ffffff;
        }
        /* 选项卡 */
        .layui-tab-brief{
            color:#61637c;
        }
        .layui-tab-title{
            color:#61637c;
        }
        .layui-tab-brief>.layui-tab-more li.layui-this:after,.layui-tab-brief>.layui-tab-title .layui-this:after{
            border:none;
            border-radius:0;
            border-bottom:2px solid rgb(245, 152, 65)
        }
        .layui-this{
            color: #55587e;
            font-weight: bold;
        }
        /* 列表list */
        .list{
            margin: 20px 40px;
        }
        ul.pagination {
            display: inline-block;
            padding: 0;
            margin: 0;
        }

        ul.pagination li {display: inline;}

        ul.pagination li a {
            color: black;
            float: left;
            padding: 8px 16px;
            text-decoration: none;
        }

        ul.pagination li a.active {
            background-color: #55587e;
            color: white;
        }
        .layui-off-content{
            display: none;
        }
</style>

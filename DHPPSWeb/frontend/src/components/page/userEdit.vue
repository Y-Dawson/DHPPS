<template>
  <!-- 实现了生日日期选择，没有实现输入框校验！！！ -->
    <div id="app">
        <div class="layui-layout layui-layout-admin">
            <!-- 导航栏 -->
            <topBar layoutName='后台管理系统' :userId="userId"></topBar>
        
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
                                <dd><router-link :to="{path:'/caseManagement',query:{uI:this.userId}}">案例管理</router-link></dd>
                                <dd><router-link :to="{path:'/modelView',query:{uI:this.userId}}">模型查看</router-link></dd>
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
                            <li><router-link :to="{path:'/userManagement',query:{uI:this.userId}}">用户管理</router-link></li>
                            <li class="layui-this" style="color: #55587e;">用户编辑</li>
                        </ul>
                    <div class="layui-tab-content">
                    <!-- 编辑部分 -->
                    <ul style="margin: 0px 50px;font-size: 14px;">
                        <li style="margin-top:20px;">
                            <div class="userName">用户名称：{{editName}}</div>
                        </li>
                        <li style="margin-top:20px;">
                            <div class="userTed">用户手机号：{{editTel}}</div>
                        </li>
                        <li style="margin-top:20px;">
                          <label class="remark">备注：</label>
                          <div style="margin-top:20px;">
                                <textarea id="desc" placeholder="请输入备注内容..." v-model="content" class="layui-textarea" style="width:500px"></textarea>
                          </div>
                          <!-- <div>{{desc}}</div> -->
                          <div style="margin-top:20px;">
                            <button type="submit"  @click="isEmpty(userid)" >立即提交</button>
                            <button type="reset"  @click="empty">重置</button>
                          </div>
                        </li>
                        <li style="margin-top:20px;">
                            <label class="authority">更改权限设置： </label>
                            <select id="selected" v-model="selected" name="authority">
                                <option value="普通用户">普通用户</option>
                                <option value="管理员">管理员</option>
                            </select>
                            <button @click="authorityIsEmpty(userid)" >确定</button>
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
import topBar from '../common/topBar.vue';
export default {
    name:'userEdit',
    components:{
      topBar
    },
    data() {
      return {
        userId:this.$route.query.userId,
        editTel:this.$route.query.uT,
        editName:this.$route.query.uN,
        userid:this.$route.query.uI,
        usercreate:this.$route.query.uC
    }
  },
  methods: {
    getParams() {
      let editTel=this.$router.query.uT;
      let editName=this.$router.query.uN;
      let userid=this.$router.query.uI;
      let usercreate=this.$route.query.uC
    },
    empty() {
      $("#desc").val("");
    },
    isEmpty(uI){
      if($("#desc").val()=="") this.$message("请输入备注信息");
      else this.putContent(uI);
    },
    putContent(uI) {
        var self = this;
        axios
          .put('http://127.0.0.1:8000/backend/accountInfo/'+uI+'/',{
            createdate: self.createdate,
            remark:$("#desc").val()
            // themeno: 1
          })
          .then(response => (
            self.content = response,
            this.$message("修改备注成功")
            // alert(JSON.stringify(response))
          ))
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
      },
      authorityIsEmpty(uI) {
        if($("#selected").val()=="管理员"||$("#selected").val()=="普通用户") this.putAuthority(uI);
        else this.$message("请选择权限");
      },
      putAuthority(uI) {
        var self = this;
        axios
          .put('http://127.0.0.1:8000/backend/accountInfo/'+uI+'/',{
            createdate: "2018-2-1",
            authority:$("#selected").val(),
            // remark:$("#desc").val(),
            themeno: 1
          })
          .then(response => (
            self.content = response,
            this.$message("修改权限成功")
            // alert(JSON.stringify(response))
          ))
          .catch(function (error) {
            alert("数据发送失败");
            console.log(error.response);
          });
      }
  }
}
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
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
/* 左侧位置 */
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
</style>
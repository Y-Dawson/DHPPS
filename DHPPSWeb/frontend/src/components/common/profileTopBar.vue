<template>
  <div class="topBar">
    <div class="layui-header">
      <div class="layui-logo">LOGO</div>
      <div class="layui-logotext">高传染性疾病预测系统</div>
      <!-- <div class="layui-logo">高传染性疾病预测系统</div> -->
      <!-- 头部区域（可配合layui已有的水平导航） -->
      <ul class="layui-nav layui-layout-left">
        <li class="layui-nav-item">
          {{ layoutName }}
        </li>
      </ul>
      <ul class="layui-nav layui-layout-right">
        <li class="layui-nav-item" style="line-height: 40px">
          <router-link
            style="margin-left: 0px; float: left"
            :to="{
              path: this.adminUrl,
              query: {
                params: JSON.stringify({ userId: this.userId, casename: 999 }),
              },
            }"
            >{{ isbut }}</router-link>
          <router-link
            style="margin-left: 0px; float: left"
            :to="{
              path: '/setting',
              query: {
                params: JSON.stringify({ userId: this.userId, casename: 999 }),
              },
            }"
            >回到首页</router-link>
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
          <!-- <span>{{ list }}</span> -->
          <a href="javascript:;">
            {{ content.username }}
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "topBar",
  data() {
    return {
      adminUrl: '/UserManagement',
      content: [],
      acontent:[],
      userId:0,
      isAdmin:'',
      ifbut:'',
      // 头像
      fits: ["fill"],
      url:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg",
    };
  },
  props:{
      layoutName:String,
      userId:Number
    },
  created: function () {
    //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
    this.getAuthority(this.userId)
    this.getContent(this.userId);
  },
  methods: {
    getContent: function (userId) {
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/profile/"+userId+"/")
        .then(response => (
            self.content = response.data,
            this.url=self.content.avatar
            // alert(JSON.stringify(response.data))
          ))
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    },
    setbut:function(a){
      if(a=="普通用户"){
        this.isbut=''
      }
      else{
        this.isbut ="进入后台"
        if(a=="超级管理员"){
          this.adminUrl='/SuperUserManage'
        }
      }
    },
    getAuthority:function(userId){
      var self = this;
      axios
        .get("http://127.0.0.1:8000/backend/accountInfo/"+userId+"/")
        .then(response =>(
            self.acontent = response.data,
            self.isAdmin=self.acontent.authority,
            self.setbut(this.isAdmin)
            // alert(self.isAdmin)
            //alert(JSON.stringify(response))
        ))
        .catch(function (error) {
          // 请求失败处理
          alert("数据请求失败wdnmd");
        });
    }
  }
};
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
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
  font-size: 10px;
}
.layui-layout-admin .layui-header {
  background-color: #8b9bbd;
}
</style>


<template>
  <!-- 实现了生日日期选择，没有实现输入框校验！！！ -->
  <div id="app">
    <div class="layui-layout layui-layout-admin">
      <div class="layui-header">
        <div class="layui-logo">
          LOGO
        </div>
        <div class="layui-logotext">
          高传染性疾病预测系统
        </div>
        <!-- <div class="layui-logo">高传染性疾病预测系统</div> -->
        <!-- 头部区域（可配合layui已有的水平导航） -->
        <ul class="layui-nav layui-layout-left">
            <li class="layui-nav-item">
                个人中心
            </li>
        </ul>
        <ul class="layui-nav layui-layout-right">
          <li class="layui-nav-item" style="line-height:40px;" >
                <router-link to="/setting"  style="margin-left:10px; float:left;">回到首页</router-link>
            </li>
            <li class="layui-nav-item" style="line-height:20px;" >
              <el-avatar shape="circle" :size="30" :fit="fit" :src="url"></el-avatar>
            </li>
            <li class="layui-nav-item">
            <a href="javascript:;">
              <span>{{ content.username}}</span>
            </a>
          </li>
        </ul>
      </div>
      <div class="layui-side layui-bg-black">
        <div class="layui-side-scroll">
          <!-- 左侧导航区域（可配合layui已有的垂直导航） -->
          <ul class="layui-nav layui-nav-tree"  lay-filter="test">
            <li class="layui-nav-item layui-nav-itemed">
                <div style="text-align:center;background-color:#fff;font-size: 16px;color: rgb(132, 132, 136);">
                    <i class="layui-icon layui-icon-app" style="font-size: 20px; color:rgb(173, 173, 173);"></i>
                    系统菜单
                </div>
                <router-link :to="{path:'/profile',query:{userId:userId}}"  >个人资料</router-link>
                <dl class="layui-nav-child">
                    <dd><router-link :to="{path:'/modifyPI',query:{userId:userId}}">修改资料</router-link></dd>
                    <dd><router-link :to="{path:'/caseView',query:{userId:userId}}">案例查看</router-link></dd>
                </dl>
            </li>
          </ul>
        </div>
      </div>
      <div class="layui-body">
        <!-- 内容主体区域 -->
        <div style="padding: 15px;">
          <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
            <ul class="layui-tab-title">
              <li class="layui-this" style="color: #55587e;">个人资料</li>
            </ul>
            <div class="layui-tab-content">
              <div class="imf" style="text-align:center;">
                <ul style="position: absolute;left:40%;font-size: 14px;text-align:left;">
                    <div class="demo-fit">
                      <div class="block" v-for="fit in fits" :key="fit">
                        <el-avatar shape="circle" :size="70" :fit="fit" :src="url"></el-avatar>
                      </div>
                    </div>
                    <li style="margin-top:30px;">
                        <span class="userName">昵称：</span>
                        <span id="returnContent">{{ content.username}}</span>
                    </li>
                    <li style="margin-top:30px;">
                        <span class="phoneNumber">手机号：</span>
                        <span id="returnContent">{{ content.phonenumber}}</span>
                    </li>
                    <li style="margin-top:30px;">
                        <span class="sex">性别：</span>
                        <span id="returnContent">{{ content.sex}}</span>
                    </li>
                    <li style="margin-top:30px;">
                        <span class="birth">生日：</span>
                        <span id="returnContent">{{ content.birth}}</span>
                    </li>
                    <li style="margin-top:30px;">
                        <span class="phoneNumber">邮箱：</span>
                        <span id="returnContent">{{ content.email}}</span>
                    </li>
                    <li style="margin-top:30px;">
                        <span class="phoneNumber">住址：</span>
                        <span id="returnContent">{{ content.address}}</span>
                    </li>
                  <el-form>
                  <el-form-item style="margin-left:-70px;">
                    <el-button  type="primary" @click="submitForm('ruleForm')">修改密码</el-button>
                    <el-button class="reset"  @click="resetForm('ruleForm')">注销</el-button>
                  </el-form-item>
                </el-form>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</div>
</template>

<script src="../assets/layui/layui.js"></script>
<script>
export default {
    name: 'profile',
    data: function () {
      return {
        userId:7,
        // 传参
        content: [],
        // 头像
        fits: ['fill'],
        url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        // 设置单选默认值
      };
    },
    created: function () {
      //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
      this.getContent(this.userId)
    },
    methods: {
      getContent: function (userId) {
        var self = this;
        axios
          .get('http://127.0.0.1:8000/backend/profile/'+userId+'/')
          .then(response => (
            self.content = response.data
            // alert(JSON.stringify(response))
          ))
          .catch(function (error) { // 请求失败处理
            alert("数据请求失败wdnmd");
          });
      },
      putContent: function () {
        var self = this;
        var date = $("#input1").val();
        axios
          .post('http://127.0.0.1:8000/backend/accountInfo/',{
            createdate: "2018-1-1"
          })
          .then(response => (
            self.content = response
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
<style>

.el-checkbox :hover{
  background: #8b9bbd;
}
</style>

<style scoped>
@import "../../assets/layui/css/layui.css";
.imf{
  margin-top:20px;
}
.el-form {
  text-align:center;
}
.el-form-item{
  margin-top: 20px;
  width: 320px;
}
.el-button--primary{
  margin-top: 30px;
  background: #bec1f0;
  border:0px;
  width: 80px;
  height: 30px;
}

.reset{
  background: #fff;
  border:1px #55587e solid;
}


.list{
  text-align:center;
  margin: 10px 300px;
}
/* 表单 */
.el-form {
  text-align:center;
}
.el-form-item{
  margin-top: 20px;
  width: 320px;
}


/* el按钮 */
.el-button{
  margin-top: 30px;
  background: #55587e;
  border:0px;
  width: 80px;
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
            font-weight: bold;
            background-color: rgb(131, 137, 158);
        }
        .layui-nav-tree .layui-nav-item a:hover{background-color:#55587e}
        /* 第二三块的字体 */
        .layui-nav-tree .layui-nav-child a{
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
            font-size: 10px;
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
        .layui-form-label{
          text-align: left;
          width: 45px;
        }
        /* 按钮 */
        .layui-btn{
          background-color: #55587e;
        }
        .layui-btn-primary{
          background-color: #fff;
        }
</style>

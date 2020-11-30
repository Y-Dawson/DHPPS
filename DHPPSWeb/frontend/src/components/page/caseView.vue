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
                        <a href="javascript:;" style="test-align:center;">回到首页</a>
                    </li>
                    <li class="layui-nav-item" style="line-height:20px;" >
                    <el-avatar shape="circle" :size="30" :fit="fit" :src="url"></el-avatar>
                    </li>
                    <li class="layui-nav-item">
                    <a href="javascript:;">
                    <span>用户名</span>
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
                        <dl class="layui-nav-child">
                            <dd><router-link to="/profile">个人资料</router-link></dd>
                            <dd><router-link to="/modifyPI">修改资料</router-link></dd>
                        </dl>
                        <router-link to="/caseView">案例查看</router-link>
                    </li>
                </ul>
                </div>
            </div>
            <div class="layui-body">
                <!-- 内容主体区域 -->
                <div style="padding: 15px;">
                <div class="layui-tab layui-tab-brief" lay-filter="docDemoTabBrief">
                    <ul class="layui-tab-title">
                    <li class="layui-this" style="color: #55587e;">案例查看</li>
                    </ul>
                    <div class="layui-tab-content">
                        <div class="box" style="text-align:center;">
                            <!-- 搜索框 --><!-- 
                            <div class="layui-form-item" style="margin: 50px;">
                                <div class="layui-input-inline" style="width: 200px;">
                                    <el-input size="small" clearable="true" v-model="input" placeholder="请输入案例名称"></el-input>
                                </div>
                                <el-button style="background:#fff;border:0px;margin:0px;">
                                    <i class="layui-icon layui-icon-search" style="font-size: 30px; color: #535357;"></i>
                                </el-button>
                            </div>
                             -->
                            <div class="box-card-group" style="margin-left:60px; margin-top:20px;width:auto;height:450px;text-align:left;">
                                <el-col :span="7" v-for="(item,index) in currentPageData.data" :key="index" >
                                    <el-card class="box-card">
                                        <div slot="header" class="clearfix">
                                            <i class="layui-icon layui-icon-template-1" style="margin-right:10px;font-size: 40px; color:rgb(173, 173, 173);"></i>
                                            <span id="returnContent">{{ item.casename }}</span>
                                            <div style="font-size:8px;line-height:20px;float:right;text-align:right">
                                              <a href="javascript:;" style="font-size:8px;color:#8b9bbd">进入编辑</a>
                                              <br>
                                              <el-button id="delete" type="text" style="font-size:8px;color:rgb(221, 0, 0)" @click="open(item.citynumber)">删除</el-button>
                                            </div>
                                        </div>
                                        <dl class="box-text">
                                          <!-- <span>{{casenum}}</span> -->
                                          <span>初始城市数量：</span>
                                          <span id="returnContent">{{ item.citynumber }}</span>
                                          <br>
                                          <span>初始道路数量：</span>
                                          <span id="returnContent">{{ item.roadnumber }}</span>
                                          <br>
                                          <span>初始总人口：</span>
                                          <span id="returnContent">{{ item.inittotal }}</span>
                                          <br>
                                          <span>初始感染人口：</span>
                                          <span id="returnContent">{{ item.inittotalinfected }}</span>
                                            <!-- <span id="returnContent" style="color:black;">{{ ccontent.themename }}</span> -->
                                            <!-- <span id="returnContent">{{ content }}</span> -->
                                            <!-- <span id="returnContent">{{ content.themeno }}</span> -->
                                        </dl>
                                    </el-card>
                                </el-col>
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
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
  name: 'caseView',
  inject:['reload'],
  data: function () {
    return {
      // 传参
      userid:1,
      contentList:[],
      isBackground:true,
      casenum:8,
      test:0,
      // 头像
      fits: ['fill'],
      url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      //分页
      totalPage: 1, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 6, // 每页显示数量
      currentPageData: [] //当前页显示内容
    }
  },
  
  mounted: function () {
    // this.getcasenum(this.userid)
    this.getCaseContent()
    this.setPages()
  },
  methods: {
    //上一页
    prevPage() {
      if (this.currentPage == 1) return;
      this.currentPage--;
      this.getCaseContent();  
      },
    // 下一页
    nextPage() {
      if (this.currentPage == this.totalPage) return ;
        this.currentPage++;
        this.getCaseContent();   
    },
    setPages(){
      if(this.totalPage<1) totalPage=1
    },
    //获取案例内容
    getCaseContent: function () {
      var self = this
      axios
        .get('http://127.0.0.1:8000/backend/case/',{
            params:{
              userid: 1,
              page_size: 6,
              page: self.currentPage
            }
          })
        .then(response => (
          self.currentPageData = response.data,
          self.totalPage=Math.ceil(self.currentPageData.pagination/self.pageSize)
          // alert(JSON.stringify(this.currentPageData))
        ))
        .catch(function (error) { // 请求失败处理
          alert('数据请求失败wdnmd')
        })
    },
    deleteCaseContent: function (id) {
      var self = this
      axios
        .delete('http://127.0.0.1:8000/backend/case/'+id,{
          })
        .then(response => (
          self.currentPageData = response.data
          // alert(JSON.stringify(this.currentPageData))
        ))
        .catch(function (error) { // 请求失败处理
          alert('数据请求失败wdnmd')
        })
    },
    open(id) {
        this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          this.deleteCaseContent(id),
          this.getCaseContent(),
          this.reload(),
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
          this.getCaseContent()
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
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
  margin-left: -70px;
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
            font-size: 10px;
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

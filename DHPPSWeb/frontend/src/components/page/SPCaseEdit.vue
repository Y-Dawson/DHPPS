<template>
  <!-- 实现了生日日期选择，没有实现输入框校验！！！ -->
    <div id="app">
        <div class="layui-layout layui-layout-admin">
            <!-- 导航栏 -->
            <topBar layoutName='后台管理系统' userId='11'></topBar>
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
                            <dd><router-link to='/SPUserManage'>信息管理</router-link></dd>
                        </dl>
                        <a class="" href="javascript:;" >案例管理</a>
                        <dl class="layui-nav-child">
                            <dd><a href="javascript:;">模型查看</a></dd>
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
                      <li class="layui-off"><router-link to='/SPCaseManage'>案例管理</router-link></li>
                      <li class="layui-this" style="color: #55587e;">案例参数</li>
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
                              <!-- <a href="javascript:;" style="font-size:8px;float:right;color:#8b9bbd">进入编辑</a> -->
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
                  <div class="layui-footer">
                    <!-- 底部固定区域 -->
                    © layui.com - 底部固定区域
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
  name: 'SPCaseEdit',
  components:{
      topBar
    },
  data: function () {
    return {
        userId:this.$route.query.userId,
      // 传参
      userid:this.$route.query.uI,
      contentList:[],
      isBackground:true,
      casenum:8,
      test:0,
      // 头像
      fits: ['fill'],
      url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      //分页
      totalPage: 2, // 统共页数，默认为1
      currentPage: 1, //当前页数 ，默认为1
      pageSize: 6, // 每页显示数量
      currentPageData: [], //当前页显示内容
      paginate: 10
    }
  },
  
  mounted: function () {
    // this.getcasenum(this.userid)
    this.getCaseContent()
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
    //获取案例内容
    getCaseContent: function () {
      var self = this;
      // alert(self.userid);
      axios
        .get('http://127.0.0.1:8000/backend/case/',{
            params:{
              userid: self.userid,
              page_size: 6,
              page: self.currentPage
            }
          })
        .then(response => (
          self.currentPageData = response.data,
          self.paginate=response.data.pagination,
          self.pageSize=response.data.pageSize,
          self.totalPage=Math.ceil(self.paginate / self.pageSize),
          this.testPage()
          // alert(JSON.stringify(this.currentPageData))
        ))
        .catch(function (error) { // 请求失败处理
          alert('数据请求失败wdnmd')
        })
    },
    testPage:function(){
      if(this.totalPage==0) this.totalPage=1;
    }
  }
}
</script>

<style scoped>
@import "../../assets/layui/css/layui.css";
/* 列表大小 */
.list{
  text-align:center;
  margin: 20px 40px;
}
/* 分页 */
.paginate{
  /* margin-top: 20px; */
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

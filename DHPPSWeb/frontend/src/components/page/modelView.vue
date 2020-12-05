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
                            <dl class="layui-nav-child">
                                <dd><router-link :to="{path:'/userManagement',query:{uI:this.userId}}">信息管理</router-link></dd>
                                <dd><router-link :to="{path:'/caseManagement',query:{uI:this.userId}}">案例管理</router-link></dd>
                            </dl>
                            <a class="" href="javascript:;" >模型查看</a>
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
                            <li class="layui-this" style="color: #55587e;">模型查看</li>
                            <!-- <li class="layui-off">用户编辑</li> -->
                        </ul>
                    </div>
                    <div class="slide" v-on:mouseover="stop()" v-on:mouseout="move()">
                        <div class="slideshow">
                            <transition-group tag="ul" name="image">
                                <li v-for="(img, index) in imgArray" v-show="index===mark" :key="index">
                                    <a href="#">
                                        <img :src='img'>
                                    </a>
                                </li>
                            </transition-group>
                        </div>
                        <div class="bar">
                            <span v-for="(item, index) in imgArray" :class="{ 'active':index===mark }"
                            @click="change(index)" :key="index"></span>
                        </div>
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
    name:'modelView',
    components:{
      topBar
    },
    data() {
      return {
        userId:this.$route.query.uI,
        //轮播图图片索引
        mark:0,
        //定时器
        timer:null,
        imgArray: [
            require('../../assets/img/picture1.jpg'),
            require('../../assets/img/picture2.jpg'),
            require('../../assets/img/picture3.jpg'),
            require('../../assets/img/picture4.jpg'),
        ]
      };
    },
    created: function () {
      //为了在内部函数能使用外部函数的this对象，要给它赋值了一个名叫self的变量。
      this.play()
    },
    methods: {
        autoPlay () {
            this.mark++;
            if (this.mark === 4) { //当遍历到最后一张图片置零
                this.mark = 0
            }
        },
        play () {
            this.timer = setInterval(this.autoPlay, 2500)
        },
        change (i) {
            this.mark = i
        },
        stop () {
            clearInterval(this.timer)
        },
        move () {
            this.timer = setInterval(this.autoPlay, 2500)
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
/* 轮播图 */
* {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .slide {
    width: 1024px;
    height: 320px;
    margin: 0 auto;
    margin-top: 50px;
    overflow: hidden;
    position: relative;
  }
  .slideshow {
    width: 1024px;
    height: 320px;
  }
  li {
    position: absolute;
  }
  img {
    width: 1024px;
    height: 320px;
  }
  .bar {
    position: absolute;
    width: 100%;
    bottom: 10px;
    margin: 0 auto;
    z-index: 10;
    text-align: center;
  }
  .bar span {
    width: 20px;
    height: 5px;
    border: 1px solid;
    background: white;
    display: inline-block;
    margin-right: 10px;
  }
  .active {
    background: #55587e !important;
  }
  
  .image-enter-active {
    transform: translateX(0);
    transition: all 1.5s ease;
  }
  .image-leave-active {
    transform: translateX(-100%);
    transition: all 1.5s ease;
  }
  .image-enter {
    transform: translateX(100%);
  }
  .image-leave {
    transform: translateX(0);
  }
</style>

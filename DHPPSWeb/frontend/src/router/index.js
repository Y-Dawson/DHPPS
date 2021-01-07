import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
const Login =()=>import("@/components/page/Login")
const signup =()=>import("@/components/page/signup")
const setting =()=>import("@/components/page/setting")
const forgetPass =()=>import("@/components/page/forgetPass")
const simulation =()=>import("@/components/page/simulation")
const AdminUserManage =()=>import("@/components/page/AdminUserManage")
const AdminCaseManage =()=>import("@/components/page/AdminCaseManage")
const AdminIndex =()=>import("@/components/page/AdminIndex")
const UserProfile =()=>import("@/components/page/UserProfile")
const UserProfileEdit =()=>import("@/components/page/UserProfileEdit")
const SuperUserManage =()=>import("@/components/page/SuperUserManage")
const AdminModelView =()=>import("@/components/page/AdminModelView")
const UserCase =()=>import("@/components/page/UserCase")
const settingMap =()=>import("@/components/page/settingMap")
const simulationMap =()=>import("@/components/page/simulationMap")
const UserIndex =()=>import("@/components/page/UserIndex")

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component:Login
    },
    {path:'/Login', component: Login},
    {path:'/signup', component: signup},
    {path:'/setting',component:setting},
    {path:'/forgetPass',component:forgetPass},
    {path:'/simulation',component:simulation},
    {path:'/AdminUserManage',component:AdminUserManage},
    {path:'/AdminCaseManage',component:AdminCaseManage},
    {path:'/AdminIndex',component:AdminIndex},
    {path:'/UserProfile',component:UserProfile},
    {path:'/UserProfileEdit',component:UserProfileEdit},
    {path:'/SuperUserManage',component:SuperUserManage},
    {path:'/AdminModelView',component:AdminModelView},
    {path:'/UserCase',component:UserCase},
    {path:'/settingMap',component:settingMap},
    {path:'/simulationMap',component:simulationMap},
    {path:'/UserIndex',component:UserIndex},
  ]
})

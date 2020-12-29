import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/page/Login'
import signup from '@/components/page/signup'
import setting from '@/components/page/setting'
import forgetPass from '@/components/page/forgetPass'
import simulation from '@/components/page/simulation'
import AdminUserManage from '@/components/page/AdminUserManage'
import AdminCaseManage from '@/components/page/AdminCaseManage'
import AdminIndex from '@/components/page/AdminIndex'
import UserProfile from '@/components/page/UserProfile'
import UserProfileEdit from '@/components/page/UserProfileEdit'
import SuperIndex from '@/components/page/SuperIndex'
import SuperUserManage from '@/components/page/SuperUserManage'
import SuperCaseManage from '@/components/page/SuperCaseManage'
import UserCase from '@/components/page/UserCase'
import settingMap from '@/components/page/settingMap'
import simulationMap from '@/components/page/simulationMap'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
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
    {path:'/SuperIndex',component:SuperIndex},
    {path:'/SuperUserManage',component:SuperUserManage},
    {path:'/SuperCaseManage',component:SuperCaseManage},
    {path:'/UserCase',component:UserCase},
    {path:'/settingMap',component:settingMap},
    {path:'/simulationMap',component:simulationMap},
  ]
})

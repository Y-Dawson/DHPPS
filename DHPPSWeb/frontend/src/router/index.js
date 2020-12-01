import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/page/Login'
import modifyPI from '@/components/page/modifyPI'
import profile from '@/components/page/profile'
import caseView from '@/components/page/caseView'
import signup from '@/components/page/signup'
import userManagement from '@/components/page/userManagement'
import userEdit from '@/components/page/userEdit'
import caseManagement from '@/components/page/caseManagement'
import caseEdit from '@/components/page/caseEdit'
import SPUserManage from '@/components/page/SPUserManage'
import SPStaffManage from '@/components/page/SPStaffManage'
import SPEdit from '@/components/page/SPEdit'
import SPCaseManage from '@/components/page/SPCaseManage'
import SPCaseEdit from '@/components/page/SPCaseEdit'
import setting from '@/components/page/setting'
import changePass from '@/components/page/changePass'
import forgetPass from '@/components/page/forgetPass'
import simulation from '@/components/page/simulation'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {path:'/modifyPI', component:modifyPI},
    {path:'/profile', component:profile},
    {path:'/Login', component: Login},
    {path:'/caseView', component: caseView},
    {path:'/signup', component: signup},
    {path:'/userManagement', component: userManagement},
    {path:'/userEdit', component: userEdit},
    {path:'/caseManagement', component: caseManagement},
    {path:'/caseEdit', component: caseEdit},
    {path:'/SPUserManage', component: SPUserManage},
    {path:'/SPStaffManage', component: SPStaffManage},
    {path:'/SPEdit', component: SPEdit},
    {path:'/SPCaseManage', component: SPCaseManage},
    {path:'/SPCaseEdit', component: SPCaseEdit},
    {path:'/setting',component:setting},
    {path:'/changePass',component:changePass},
    {path:'/forgetPass',component:forgetPass},
    {path:'/simulation',component:simulation}
  ]
})

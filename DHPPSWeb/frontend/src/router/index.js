import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/page/Login'
import modifyPI from '@/components/page/modifyPI'
import profile from '@/components/page/profile'
import caseView from '@/components/page/caseView'
import signup from '@/components/page/signup'
import UserManagement from '@/components/page/UserManagement'
import UserEdit from '@/components/page/UserEdit'
import CaseManagement from '@/components/page/CaseManagement'
import CaseEdit from '@/components/page/CaseEdit'
import SuperUserManage from '@/components/page/SuperUserManage'
import SuperStaffManage from '@/components/page/SuperStaffManage'
import SuperEdit from '@/components/page/SuperEdit'
import SuperCaseManage from '@/components/page/SuperCaseManage'
import SuperCaseEdit from '@/components/page/SuperCaseEdit'
import setting from '@/components/page/setting'
import changePass from '@/components/page/changePass'
import forgetPass from '@/components/page/forgetPass'
import simulation from '@/components/page/simulation'
import ModelView from '@/components/page/ModelView'
import SuperModelView from '@/components/page/SuperModelView'
// import uploadTest from '@/components/page/uploadTest'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    // {patht:'/uploadTest',component:uploadTest},
    {path:'/modifyPI', component:modifyPI},
    {path:'/profile', component:profile},
    {path:'/Login', component: Login},
    {path:'/caseView', component: caseView},
    {path:'/signup', component: signup},
    {path:'/UserManagement', component: UserManagement},
    {path:'/UserEdit', component: UserEdit},
    {path:'/CaseManagement', component: CaseManagement},
    {path:'/CaseEdit', component: CaseEdit},
    {path:'/SuperUserManage', component: SuperUserManage},
    {path:'/SuperStaffManage', component: SuperStaffManage},
    {path:'/SuperEdit', component: SuperEdit},
    {path:'/SuperCaseManage', component: SuperCaseManage},
    {path:'/SuperCaseEdit', component: SuperCaseEdit},
    {path:'/setting',component:setting},
    {path:'/changePass',component:changePass},
    {path:'/forgetPass',component:forgetPass},
    {path:'/simulation',component:simulation},
    {path:'/ModelView',component:ModelView},
    {path:'/SuperModelView',component:SuperModelView}
  ]
})

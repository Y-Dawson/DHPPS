import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import login from '@/components/page/login'
import modifyPI from '@/components/page/modifyPI'
import profile from '@/components/page/profile'
import caseView from '@/components/page/caseView'
import signup from '@/components/page/signup'
import changePass from '@/components/page/changePass'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'modifyPI',
      component: modifyPI
    },
    {path:'/modifyPI', component:modifyPI},
    {path:'/profile', component:profile},
    {path:'/login', component:login},
    {path:'/caseView', component:caseView},
    {path:'/signup', component: signup},
    {path:'/changePass',component:changePass}

  ]
})

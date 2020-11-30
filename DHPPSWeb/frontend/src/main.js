// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import axios from 'axios'
import router from './router'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css'
axios.defaults.withCredentials = true;

Vue.use(ElementUI)
Vue.prototype.$http = axios
Vue.use(VueResource)
Vue.config.productionTip = false

axios.defaults.withCredentials = true;//允许跨域携带cookie信息

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  components: { App },
  template: '<App/>'
})

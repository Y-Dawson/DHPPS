// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import axios from 'axios'
import router from './router'
import ElementUI from 'element-ui'
// import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css'
// import VueParticles from 'vue-particles'
// Vue.use(VueParticles)

// import VueCookies from 'vue-cookies'
// Vue.use(VueCookies)

Vue.use(ElementUI)
// Vue.use(VueResource)
Vue.config.productionTip = false


axios.defaults.withCredentials = true;  //允许axios请求携带cookie等凭证
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
// 请求拦截
axios.interceptors.request.use(
  config => {
    if (store.getters.token) { // 若存在token，则每个Http Header都加上token
      config.headers.Authorization = `token ${store.getters.token}`
    }
    console.log('request请求配置', config)
    console.log(`token is ${store.getters.token}`)
    return config
  },
  err => {
    return Promise.reject(err)
  });

const service = axios.create({
  baseURL: '/backend',
  withCredentials: true
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  axios,
  components: { App },
  template: '<App/>'
})

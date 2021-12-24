"use unsafe-url";

import Vue from 'vue'
import App from './App.vue'
import {store} from './store/default'

import 'bootstrap/dist/css/bootstrap.min.css'
import BootstrapVue from 'bootstrap-vue' 


Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')

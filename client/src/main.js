import Vue from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

window.$ = require('jquery')
window.JQuery = require('jquery')

Vue.use(BootstrapVue)

Vue.config.productionTip = false

export const bus = new Vue()

new Vue({
  render: h => h(App),
}).$mount('#app')

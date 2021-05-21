import Vue from 'vue'
import App from './App.vue'
import Font from './plugins/fontAwesomeIcon.js'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

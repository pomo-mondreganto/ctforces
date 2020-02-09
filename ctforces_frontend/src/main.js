import Vue from 'vue';
import Fragment from 'vue-fragment';
import Toasted from 'vue-toasted';
import VueSimplemde from 'vue-simplemde';
import App from './App.vue';
import router from './router';
import store from './store';

import { apiUrl } from '@/config';
import axios from 'axios';

Vue.config.productionTip = false;

axios.defaults.baseURL = apiUrl;
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

axios.interceptors.response.use(
    response => response,
    error => {
        const ret = error;
        if (!ret.response) {
            ret.response = { data: { detail: 'Api server is down' } };
        } else if (ret.response.status === 500) {
            ret.response.data = { detail: 'Api server is down' };
        }
        return Promise.reject(ret);
    }
);

Vue.prototype.$http = axios;
store.$http = axios;

Vue.use(Fragment.Plugin);
Vue.use(Toasted, {
    position: 'bottom-right',
    duration: 2000,
    keepOnHover: true,
});

Vue.component('vue-simplemde', VueSimplemde);

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');

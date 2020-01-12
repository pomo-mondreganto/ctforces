import Vue from 'vue';
import Fragment from 'vue-fragment';
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
        if (ret.response.status === 500) {
            ret.response.data = { detail: 'Api server is down' };
        }
        return Promise.reject(ret);
    }
);

Vue.prototype.$http = axios;
store.$http = axios;

Vue.use(Fragment.Plugin);

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');

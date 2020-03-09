import Vue from 'vue';
import Toasted from 'vue-toasted';
import VueSimplemde from 'vue-simplemde';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import Paginate from 'vuejs-paginate';
import lodash from 'lodash';

import App from './App.vue';
import router from './router';
import store from './store';

import { apiUrl } from '@/config';
import axios from 'axios';
import parse from '@/utils/errorParser';
import {
    isArray,
    isBoolean,
    isFunction,
    isNull,
    isNumber,
    isObject,
    isRegExp,
    isString,
    isUndefined,
} from '@/utils/types';

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

Vue.prototype._ = lodash;
Vue.prototype.$http = axios;
Vue.prototype.$parse = parse;
Vue.prototype.$types = {
    isArray,
    isBoolean,
    isFunction,
    isNull,
    isNumber,
    isObject,
    isRegExp,
    isString,
    isUndefined,
};
store.$http = axios;

Vue.use(Toasted, {
    position: 'bottom-right',
    duration: 2000,
    keepOnHover: true,
});

Vue.component('vue-simplemde', VueSimplemde);
Vue.component('datetime', VueCtkDateTimePicker);
Vue.component('paginate', Paginate);

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');

import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import { apiUrl } from '@/config';
import axios from 'axios';
import lodash from 'lodash';
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
import Toasted from 'vue-toasted';
import VueSimplemde from 'vue-simplemde';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import Paginate from 'vuejs-paginate';

import vSelect from 'vue-select';
import ProgressBar from 'vue-progressbar-component';
import Card from '@/components/Card';
import FDetail from '@/components/Form/Detail';
import User from '@/components/User';
import Team from '@/components/Team';
import Master from '@/layouts/Master';
import MasterStacked from '@/layouts/MasterStacked';
import Full from '@/layouts/Full';
import Countdown from '@/components/Countdown';

Vue.config.productionTip = false;

/* axios configuration */
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

/* utils injection */

Vue.prototype._ = lodash;
Vue.prototype.$http = axios;
Vue.prototype.$parse = parse;
Vue.prototype.$time = function(props) {
    let ret = '';
    if (props.days > 1) {
        ret += `${props.days} days `;
    } else if (props.days === 1) {
        ret += `${props.days} day `;
    }
    ret += `${props.hours.toString().padStart(2, '0')}:`;
    ret += `${props.minutes.toString().padStart(2, '0')}:`;
    ret += `${props.seconds.toString().padStart(2, '0')}`;
    return ret;
};
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
store.$parse = parse;

/* external components */

Vue.use(Toasted, {
    position: 'bottom-right',
    duration: 4000,
    keepOnHover: true,
});

Vue.component('vue-simplemde', VueSimplemde);
Vue.component('datetime', VueCtkDateTimePicker);
Vue.component('paginate', Paginate);
Vue.component('v-select', vSelect);
Vue.component('v-progress-bar', ProgressBar);

/* internal components */

Vue.component('card', Card);
Vue.component('f-detail', FDetail);
Vue.component('user', User);
Vue.component('team', Team);
Vue.component('master-layout', Master);
Vue.component('master-layout-stacked', MasterStacked);
Vue.component('full-layout', Full);
Vue.component('countdown', Countdown);

new Vue({
    router,
    store,
    render: h => h(App),
}).$mount('#app');

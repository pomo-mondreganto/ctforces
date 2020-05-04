import Vue from 'vue';
import VueRouter from 'vue-router';

import routes from './routes';
import store from '@/store';
import { isNull } from '@/utils/types';

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

router.beforeEach(async (to, from, next) => {
    if (to.meta.auth) {
        if (isNull(await store.dispatch('GET_USER'))) {
            localStorage.setItem(
                'route',
                JSON.stringify({
                    name: to.name,
                    query: to.query,
                    params: to.params,
                })
            );
            next({
                name: 'login',
            });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;

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
    scrollBehavior() {
        return { x: 0, y: 0 };
    },
});

router.beforeEach(async (to, from, next) => {
    if (to.matched.some(record => record.meta.auth)) {
        if (isNull(await store.dispatch('GET_USER'))) {
            next({
                name: 'login',
                query: { redirect: to.name },
            });
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;

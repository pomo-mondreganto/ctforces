import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null,
    },
    mutations: {
        SET_USER: (state, user) => {
            state.user = user;
        },
    },
    actions: {
        GET_ME: async function(context) {
            try {
                const r = await this.$http.get('/me/');
                context.commit('SET_USER', r.data);
            } catch {
                context.commit('SET_USER', null);
            }
        },
    },
    modules: {},
});

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: null,
        userRequested: false,
        sidebar: true,
    },
    mutations: {
        SET_USER: (state, user) => {
            state.user = user;
            state.userRequested = true;
        },

        TOGGLE_SIDEBAR: state => {
            state.sidebar = !state.sidebar;
        },
    },
    actions: {
        UPDATE_USER: async function(context) {
            try {
                const r = await this.$http.get('/me/');
                const user = r.data;
                context.commit('SET_USER', user);
            } catch {
                context.commit('SET_USER', null);
            }
        },

        GET_USER: async function(context) {
            if (context.state.userRequested) {
                return context.state.user;
            }

            await context.dispatch('UPDATE_USER');

            return context.state.user;
        },

        TOGGLE_SIDEBAR: function(context) {
            context.commit('TOGGLE_SIDEBAR');
        },
    },
    modules: {},
});

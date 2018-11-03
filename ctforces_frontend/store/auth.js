import Vuex from 'vuex';

export const state = () => ({
    authUser: null
});

export const mutations = {
    set_user: function(state, user) {
        state.authUser = user;
    }
};

export const actions = {
    async login({ commit }, { username, password }) {
        try {
            let { data } = await this.$axios.post('login/', {
                username,
                password
            });
            commit('set_user', data);
        } catch (e) {
            throw e;
        }
    },
    async logout({ commit }) {
        try {
            let { data } = await this.$axios.post('logout/');
            commit('set_user', null);
        } catch (e) {
            throw e;
        }
    }
};

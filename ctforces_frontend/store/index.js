export const state = () => ({});

export const actions = {
    async nuxtServerInit({ commit }) {
        try {
            let { data } = await this.$axios.get('/me/');
            commit('auth/set_user', data);
        } catch (e) {}
    }
};

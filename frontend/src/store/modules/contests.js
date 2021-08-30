const state = () => {
    return {
        contest: null,
        errors: [],
        runningContests: [],
        upcomingContests: [],
        finishedContests: [],
    };
};

const getters = {};

const mutations = {
    setContest: (state, contest) => {
        state.contest = contest;
    },
    setErrors: (state, errors) => {
        state.errors = errors;
    },
};

const actions = {
    fetchContest: async function({ commit }, id) {
        try {
            const { data } = await this.$http.get(`/contests/${id}/`);
            commit('setContest', data);
            commit('setErrors', []);
        } catch (error) {
            commit('setErrors', this.$parse(error.response.data));
        }
    },
};

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
};

import Vuex from 'vuex';

const createStore = () => {
    return new Vuex.Store({
        state: () => ({
            authUser: null
        }),
        mutations: {
            set_user: function({ user }) {
                state.authUser = user;
            }
        },
        actions: {
            async login({ commit }, { username, password }) {
                try {
                    console.log('asd');
                    let data = await this.$axios.post('login/', {
                        username,
                        password
                    });
                    console.log(data);
                } catch (e) {
                    console.log(e);
                }
            }
        }
    });
};

export default createStore;

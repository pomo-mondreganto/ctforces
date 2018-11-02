import Vuex from 'vuex';
import axios from 'axios';

const createStore = () => {
    return new Vuex.Store({
        state: () => ({
          authUser: null
        }),
        mutations: {
          set_user: function ({user}) {
            authUser = user;
          }
        },
      actions: {
        async login({commit}, {username, password}) {
          try {
            let data = await axios.post('/api/login/', {username, password});
            console.log(data);
          } catch (e) {
            console.log(e);
          }
            }
        }
    });
};

export default createStore;

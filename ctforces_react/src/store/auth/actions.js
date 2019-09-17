import { createActions } from 'reduxsauce';

const { Types, Creators } = createActions({
    updateAuthUser: {
        user: null,
        loggedIn: false,
        requested: false,
    },
});

export { Types, Creators };

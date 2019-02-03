import { createReducer } from 'reduxsauce';
import { Types as ReduxSauceTypes } from 'reduxsauce';

import { Types } from './actions';

const INITIAL_STATE = {
    user: null,
    loggedIn: false,
    requested: false
};

const updateUser = (state = INITIAL_STATE, action) => {
    return {
        ...state,
        user: action.user,
        loggedIn: action.loggedIn,
        requested: action.requested
    };
};

const HANDLERS = {
    [Types.UPDATE_AUTH_USER]: updateUser
};

export default createReducer(INITIAL_STATE, HANDLERS);

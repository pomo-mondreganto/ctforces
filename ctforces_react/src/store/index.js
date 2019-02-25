import { combineReducers } from 'redux';
import authReducers from './auth/reducers';

const rootReducer = combineReducers({
    auth: authReducers,
});

export default rootReducer;

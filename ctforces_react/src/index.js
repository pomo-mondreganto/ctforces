import React from 'react';
import { render } from 'react-dom';
import { Provider } from 'react-redux';
import rootReducer from './store';
import App from './pages';
import { createStore } from 'redux';
import axios from 'axios';
import { api_url } from '../config/config';

import './styles/index.scss';

axios.defaults.baseURL = api_url;
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const store = createStore(rootReducer);

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);

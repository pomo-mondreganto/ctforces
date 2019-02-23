import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import UserPage from './index/Container';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from '../../lib/Routes';

const Users = () => {
    return (
        <Switch>
            <PublicRoute exact path="/users/:username/" component={UserPage} />
        </Switch>
    );
};

export default Users;

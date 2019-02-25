import React from 'react';
import { Switch } from 'react-router-dom';
import UserPage from './index/Container';

import { PublicRoute } from '../../lib/Routes';

const Users = () => (
    <Switch>
        <PublicRoute exact path="/users/:username/" component={UserPage} />
    </Switch>
);

export default Users;

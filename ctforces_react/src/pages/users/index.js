import React from 'react';
import { Switch } from 'react-router-dom';
import UserPage from './index/Container';
import TasksListPage from './tasks_list/Container';
import RatingTopPage from './top_rating_list/Container';
import UpsolvingTopPage from './top_upsolving_list/Container';

import { PublicRoute } from '../../lib/Routes';

const Users = () => (
    <Switch>
        <PublicRoute exact path="/users/:username/" component={UserPage} />
        <PublicRoute exact path="/users/:username/tasks/" component={TasksListPage} />
        <PublicRoute exact path="/users/rating/top/" component={RatingTopPage} />
        <PublicRoute exact path="/users/upsolving/top/" component={UpsolvingTopPage} />
    </Switch>
);

export default Users;

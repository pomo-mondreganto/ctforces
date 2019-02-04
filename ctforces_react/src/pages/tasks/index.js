import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import TaskCreatePage from './create/Container';
// import TaskViewPage from './index/Container';
// import TaskEditPage from './edit/Container';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from '../../lib/Routes';

const Posts = () => {
    return (
        <Switch>
            <PrivateRoute
                exact
                path="/tasks/create"
                component={TaskCreatePage}
            />
            {/* <PublicRoute exact path="/tasks/:id" component={PostViewPage} />
            <PrivateRoute
                exact
                path="/tasks/:id/edit"
                component={PostEditPage}
            /> */}
        </Switch>
    );
};

export default Posts;

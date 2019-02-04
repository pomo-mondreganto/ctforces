import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import PostCreatePage from './create/Container';
import PostViewPage from './index/Container';
import PostEditPage from './edit/Container';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from '../../lib/Routes';

const Posts = () => {
    return (
        <Switch>
            <PrivateRoute
                exact
                path="/posts/create"
                component={PostCreatePage}
            />
            <PublicRoute exact path="/posts/:id" component={PostViewPage} />
            <PrivateRoute
                exact
                path="/posts/:id/edit"
                component={PostEditPage}
            />
        </Switch>
    );
};

export default Posts;

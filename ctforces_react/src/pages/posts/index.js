import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import PostCreatePage from './create/Container';

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
        </Switch>
    );
};

export default Posts;

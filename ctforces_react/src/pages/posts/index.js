import React from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';
import PostCreatePage from './create/Container';
import PostViewPage from './index/Container';
import PostEditPage from './edit/Container';


const Posts = () => (
    <Switch>
        <PrivateRoute
            exact
            path="/posts/create/"
            component={PostCreatePage}
        />
        <PublicRoute exact path="/posts/:id/" component={PostViewPage} />
        <PrivateRoute
            exact
            path="/posts/:id/edit/"
            component={PostEditPage}
        />
    </Switch>
);

export default Posts;

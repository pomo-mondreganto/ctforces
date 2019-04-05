import React from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';
import PostCreatePage from './create/Container';
import PostViewPage from './index/Container';
import PostEditPage from './edit/Container';


const Posts = props => (
    <Switch>
        <PrivateRoute
            exact
            path="/posts/create/"
            component={PostCreatePage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute exact path="/posts/:id/" component={PostViewPage} key={props.location.pathname + props.location.search} />
        <PrivateRoute
            exact
            path="/posts/:id/edit/"
            component={PostEditPage}
            key={props.location.pathname + props.location.search}
        />
    </Switch>
);

export default Posts;

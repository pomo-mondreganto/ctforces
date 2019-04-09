import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';

const PostCreatePage = lazy(() => import('./create/Container'));
const PostViewPage = lazy(() => import('./index/Container'));
const PostEditPage = lazy(() => import('./edit/Container'));


const Posts = props => (
    <Suspense fallback={<div>Loading...</div>}>
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
    </Suspense>
);

export default Posts;

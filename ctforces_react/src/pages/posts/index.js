import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';

const PostCreatePage = lazy(() => import('./create/Container'));
const PostViewPage = lazy(() => import('./index/Container'));
const PostEditPage = lazy(() => import('./edit/Container'));


const Posts = () => (
    <Suspense fallback={<div>Loading...</div>}>
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
    </Suspense>
);

export default Posts;

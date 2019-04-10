import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';
import { PublicRoute } from 'lib/routes';

const ContestsListPage = lazy(() => import('./contests_list/Container'));
const RatingTopPage = lazy(() => import('./top_rating_list/Container'));
const UpsolvingTopPage = lazy(() => import('./top_upsolving_list/Container'));
const PostsListPage = lazy(() => import('./posts_list/Container'));
const TasksListPage = lazy(() => import('./tasks_list/Container'));
const UserPage = lazy(() => import('./index/Container'));

const Users = () => <Suspense fallback={<div>Loading...</div>}>
    <Switch>
        <PublicRoute exact path="/users/:username/" component={UserPage} />
        <PublicRoute exact path="/users/:username/tasks/" component={TasksListPage} />
        <PublicRoute exact path="/users/:username/posts/" component={PostsListPage} />
        <PublicRoute exact path="/users/:username/contests/" component={ContestsListPage} />
        <PublicRoute exact path="/users/rating/top/" component={RatingTopPage} />
        <PublicRoute exact path="/users/upsolving/top/" component={UpsolvingTopPage} />
    </Switch>
</Suspense>;

export default Users;

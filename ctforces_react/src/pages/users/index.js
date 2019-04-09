import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';
import { PublicRoute } from 'lib/Routes';

const ContestsListPage = lazy(() => import('./contests_list/Container'));
const RatingTopPage = lazy(() => import('./top_rating_list/Container'));
const UpsolvingTopPage = lazy(() => import('./top_upsolving_list/Container'));
const PostsListPage = lazy(() => import('./posts_list/Container'));
const TasksListPage = lazy(() => import('./tasks_list/Container'));
const UserPage = lazy(() => import('./index/Container'));

const Users = props => <Suspense fallback={<div>Loading...</div>}>
    <Switch>
        <PublicRoute exact path="/users/:username/" component={UserPage} key={props.location.pathname + props.location.search} />
        <PublicRoute exact path="/users/:username/tasks/" component={TasksListPage} key={props.location.pathname + props.location.search} />
        <PublicRoute exact path="/users/:username/posts/" component={PostsListPage} key={props.location.pathname + props.location.search} />
        <PublicRoute exact path="/users/:username/contests/" component={ContestsListPage} key={props.location.pathname + props.location.search} />
        <PublicRoute exact path="/users/rating/top/" component={RatingTopPage} key={props.location.pathname + props.location.search} />
        <PublicRoute exact path="/users/upsolving/top/" component={UpsolvingTopPage} key={props.location.pathname + props.location.search} />
    </Switch>
</Suspense>;

export default Users;

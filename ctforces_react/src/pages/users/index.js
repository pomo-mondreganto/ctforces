import React from 'react';
import { Switch } from 'react-router-dom';
import { PublicRoute } from 'lib/Routes';
import UserPage from './index/Container';
import TasksListPage from './tasks_list/Container';
import PostsListPage from './posts_list/Container';
import ContestsListPage from './contests_list/Container';
import RatingTopPage from './top_rating_list/Container';
import UpsolvingTopPage from './top_upsolving_list/Container';


const Users = props => (
    <Switch>
        <PublicRoute exact path="/users/:username/" component={UserPage} key={props.location.pathname} />
        <PublicRoute exact path="/users/:username/tasks/" component={TasksListPage} key={props.location.pathname} />
        <PublicRoute exact path="/users/:username/posts/" component={PostsListPage} key={props.location.pathname} />
        <PublicRoute exact path="/users/:username/contests/" component={ContestsListPage} key={props.location.pathname} />
        <PublicRoute exact path="/users/rating/top/" component={RatingTopPage} key={props.location.pathname} />
        <PublicRoute exact path="/users/upsolving/top/" component={UpsolvingTopPage} key={props.location.pathname} />
    </Switch>
);

export default Users;

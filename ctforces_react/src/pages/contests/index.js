import React from 'react';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from 'lib/Routes';
import ContestCreatePage from './create/Container';
import ContestViewPage from './index/Container';
import ContestEditPage from './edit/Container';
import ContestListPage from './list/Container';
import ContestScoreboardPage from './scoreboard/Container';
import ContestTaskPage from './task/Container';
import ContestTaskSolvedPage from './task_solved/Container';


const Contests = props => (
    <Switch>
        <PrivateRoute
            exact
            path="/contests/create/"
            component={ContestCreatePage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute
            exact
            path="/contests/:id/"
            component={ContestViewPage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute
            exact
            path="/contests/:id/scoreboard/"
            component={ContestScoreboardPage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute
            exact
            path="/contests/:id/tasks/:task_id/"
            component={ContestTaskPage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute
            exact
            path="/contests/:id/tasks/:task_id/solved/"
            component={ContestTaskSolvedPage}
            key={props.location.pathname + props.location.search}
        />
        <PublicRoute
            exact
            path="/contests/"
            component={ContestListPage}
            key={props.location.pathname + props.location.search}
        />
        <PrivateRoute
            exact
            path="/contests/:id/edit/"
            component={ContestEditPage}
            key={props.location.pathname + props.location.search}
        />
    </Switch>
);

export default Contests;

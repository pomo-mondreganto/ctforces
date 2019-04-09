import React, { lazy, Suspense } from 'react';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from 'lib/Routes';

const ContestCreatePage = lazy(() => import('./create/Container'));
const ContestViewPage = lazy(() => import('./index/Container'));
const ContestEditPage = lazy(() => import('./edit/Container'));
const ContestListPage = lazy(() => import('./list/Container'));
const ContestScoreboardPage = lazy(() => import('./scoreboard/Container'));
const ContestTaskPage = lazy(() => import('./task/Container'));
const ContestTaskSolvedPage = lazy(() => import('./task_solved/Container'));


const Contests = props => (
    <Suspense fallback={<div>Loading...</div>}>
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
    </Suspense>
);

export default Contests;

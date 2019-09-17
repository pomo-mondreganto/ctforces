import React, { lazy, Suspense } from 'react';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from 'lib/routes';

const ContestCreatePage = lazy(() => import('./create/Container'));
const ContestViewPage = lazy(() => import('./index/Container'));
const ContestEditPage = lazy(() => import('./edit/Container'));
const ContestListPage = lazy(() => import('./list/Container'));
const ContestScoreboardPage = lazy(() => import('./scoreboard/Container'));
const ContestTaskPage = lazy(() => import('./task/Container'));
const ContestTaskSolvedPage = lazy(() => import('./task_solved/Container'));

const Contests = () => (
    <Suspense fallback={<div>Loading...</div>}>
        <Switch>
            <PrivateRoute
                exact
                path="/contests/create/"
                component={ContestCreatePage}
            />
            <PublicRoute
                exact
                path="/contests/:id/"
                component={ContestViewPage}
            />
            <PublicRoute
                exact
                path="/contests/:id/scoreboard/"
                component={ContestScoreboardPage}
            />
            <PublicRoute
                exact
                path="/contests/:id/tasks/:task_id/"
                component={ContestTaskPage}
            />
            <PublicRoute
                exact
                path="/contests/:id/tasks/:task_id/solved/"
                component={ContestTaskSolvedPage}
            />
            <PublicRoute exact path="/contests/" component={ContestListPage} />
            <PrivateRoute
                exact
                path="/contests/:id/edit/"
                component={ContestEditPage}
            />
        </Switch>
    </Suspense>
);

export default Contests;

import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';

import 'styles/pages/tasks.scss';
import 'styles/components/LongText.scss';

const TaskEditPage = lazy(() => import('./edit/Container'));
const TaskListPage = lazy(() => import('./list/Container'));
const TaskSolvedPage = lazy(() => import('./solved/Container'));
const TaskCreatePage = lazy(() => import('./create/Container'));
const TaskViewPage = lazy(() => import('./index/Container'));

const Tasks = props => (
    <Suspense fallback={<div>Loading...</div>}>
        <Switch>
            <PrivateRoute
                exact
                path="/tasks/create/"
                component={TaskCreatePage}
                key={props.location.pathname + props.location.search}
            />
            <PublicRoute exact path="/tasks/:id/" component={TaskViewPage} key={props.location.pathname + props.location.search} />
            <PublicRoute exact path="/tasks/:id/solved/" component={TaskSolvedPage} key={props.location.pathname + props.location.search} />
            <PublicRoute exact path="/tasks/" component={TaskListPage} key={props.location.pathname + props.location.search} />
            <PrivateRoute
                exact
                path="/tasks/:id/edit/"
                component={TaskEditPage}
                key={props.location.pathname + props.location.search}
            />
        </Switch>
    </Suspense>
);

export default Tasks;

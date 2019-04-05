import React from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';
import TaskCreatePage from './create/Container';
import TaskViewPage from './index/Container';
import TaskEditPage from './edit/Container';
import TaskListPage from './list/Container';
import TaskSolvedPage from './solved/Container';

import 'styles/pages/tasks.scss';
import 'styles/components/LongText.scss';

const Tasks = props => (
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
);

export default Tasks;

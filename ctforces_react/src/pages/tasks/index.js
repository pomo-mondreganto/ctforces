import React from 'react';
import { Switch } from 'react-router-dom';

import { PublicRoute, PrivateRoute } from 'lib/Routes';
import TaskCreatePage from './create/Container';
import TaskViewPage from './index/Container';
import TaskEditPage from './edit/Container';
import TaskListPage from './list/Container';

import 'styles/pages/tasks.scss';

const Tasks = () => (
    <Switch>
        <PrivateRoute
            exact
            path="/tasks/create/"
            component={TaskCreatePage}
        />
        <PublicRoute exact path="/tasks/:id/" component={TaskViewPage} />
        <PublicRoute exact path="/tasks/" component={TaskListPage} />
        <PrivateRoute
            exact
            path="/tasks/:id/edit/"
            component={TaskEditPage}
        />
    </Switch>
);

export default Tasks;

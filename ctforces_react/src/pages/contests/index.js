import React from 'react';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from 'lib/Routes';
import ContestCreatePage from './create/Container';
import ContestViewPage from './index/Container';
import ContestEditPage from './edit/Container';
import ContestListPage from './list/Container';


const Contests = () => (
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
            path="/contests/"
            component={ContestListPage}
        />
        <PrivateRoute
            exact
            path="/contests/:id/edit/"
            component={ContestEditPage}
        />
    </Switch>
);

export default Contests;

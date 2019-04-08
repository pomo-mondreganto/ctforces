import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';

import { PrivateRoute } from 'lib/Routes';

const SocialSettingsPage = lazy(() => import('./social/Container'));
const GeneralSettingsPage = lazy(() => import('./general/Container'));


const Settings = props => (
    <Suspense fallback={<div>Loading...</div>}>
        <Switch>
            <PrivateRoute exact path="/settings/social/" component={SocialSettingsPage} key={props.location.pathname + props.location.search} />
            <PrivateRoute exact path="/settings/general/" component={GeneralSettingsPage} key={props.location.pathname + props.location.search} />
        </Switch>
    </Suspense>
);

export default Settings;

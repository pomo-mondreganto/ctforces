import React, { lazy, Suspense } from 'react';
import { Switch } from 'react-router-dom';

import { PrivateRoute } from 'lib/Routes';

const SocialSettingsPage = lazy(() => import('./social/Container'));
const GeneralSettingsPage = lazy(() => import('./general/Container'));


const Settings = () => (
    <Suspense fallback={<div>Loading...</div>}>
        <Switch>
            <PrivateRoute exact path="/settings/social/" component={SocialSettingsPage} />
            <PrivateRoute exact path="/settings/general/" component={GeneralSettingsPage} />
        </Switch>
    </Suspense>
);

export default Settings;

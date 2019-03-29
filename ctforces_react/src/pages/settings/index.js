import React from 'react';
import { Switch } from 'react-router-dom';

import { PrivateRoute } from 'lib/Routes';
import SocialSettingsPage from './social/Container';
import GeneralSettingsPage from './general/Container';


const Settings = () => (
    <Switch>
        <PrivateRoute exact path="/settings/social/" component={SocialSettingsPage} />
        <PrivateRoute exact path="/settings/general/" component={GeneralSettingsPage} />
    </Switch>
);

export default Settings;

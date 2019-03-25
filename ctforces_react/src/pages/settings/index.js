import React from 'react';
import { Switch } from 'react-router-dom';

import SocialSettingsPage from './social/Container';

import { PrivateRoute } from '../../lib/Routes';

const Settings = () => (
    <Switch>
        <PrivateRoute exact path="/settings/social" component={SocialSettingsPage} />
    </Switch>
);

export default Settings;

import React from 'react';
import { Switch } from 'react-router-dom';

import { PrivateRoute } from 'lib/Routes';
import SocialSettingsPage from './social/Container';
import GeneralSettingsPage from './general/Container';


const Settings = props => (
    <Switch>
        <PrivateRoute exact path="/settings/social/" component={SocialSettingsPage} key={props.location.pathname} />
        <PrivateRoute exact path="/settings/general/" component={GeneralSettingsPage} key={props.location.pathname} />
    </Switch>
);

export default Settings;

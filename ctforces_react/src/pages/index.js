import React, { lazy, Suspense } from 'react';

import { Switch } from 'react-router-dom';
import { PublicRoute, PrivateRoute } from 'lib/Routes';

const UsersPage = lazy(() => import('./users'));
const PostsPage = lazy(() => import('./posts'));
const TasksPage = lazy(() => import('./tasks'));
const ContestsPage = lazy(() => import('./contests'));
const ConfirmEmailPage = lazy(() => import('./confirm_email/Container'));
const ResetPasswordPage = lazy(() => import('./password_reset/Container'));
const ResetPasswordConfirmPage = lazy(() => import('./confirm_password_reset/Container'));
const RegisterPage = lazy(() => import('./register/Container'));
const SettingsPage = lazy(() => import('./settings'));
const LoginPage = lazy(() => import('./login/Container'));
const IndexPage = lazy(() => import('./index/Container'));

class App extends React.Component {
    render = () => (
        <Suspense fallback={<div>Loading...</div>}>
            <Switch>
                <PublicRoute exact path="/" component={IndexPage} isRootRoute={true} />
                <PublicRoute exact path="/login/" component={LoginPage} isRootRoute={true} />
                <PublicRoute exact path="/register/" component={RegisterPage} isRootRoute={true} />
                <PublicRoute path="/users/" component={UsersPage} isRootRoute={true} />
                <PublicRoute path="/posts/" component={PostsPage} isRootRoute={true} />
                <PublicRoute path="/tasks/" component={TasksPage} isRootRoute={true} />
                <PublicRoute path="/contests/" component={ContestsPage} isRootRoute={true} />

                <PublicRoute path="/confirm_email/" component={ConfirmEmailPage} isRootRoute={true} />
                <PublicRoute path="/reset_password/" component={ResetPasswordPage} isRootRoute={true} />
                <PublicRoute path="/reset_password_confirm/" component={ResetPasswordConfirmPage} isRootRoute={true} />

                <PrivateRoute path="/settings/" component={SettingsPage} isRootRoute={true} />
            </Switch>
        </Suspense>
    )
}

export default App;

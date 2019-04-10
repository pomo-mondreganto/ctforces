import React from 'react';

import { Route, Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';

import getMe from 'lib/getMe';

const PrivateRoute = withAuth(
    (props) => {
        const {
            component: Component,
            auth,
            isRootRoute,
            ...rest
        } = props;

        if (isRootRoute) {
            getMe(props);
        }

        if (!auth.requested) {
            return null;
        }

        return (
            <Route
                {...rest}
                render={routeRest => (auth.loggedIn ? (
                    <Component {...routeRest}
                        key={props.location.pathname + props.location.search} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/login/',
                            state: { from: props.location },
                        }}
                    />
                ))
                }
            />
        );
    },
);


const PublicRoute = withAuth(
    (props) => {
        const {
            component: Component,
            isRootRoute,
            ...rest
        } = props;

        if (isRootRoute) {
            getMe(props);
        }

        return <Route {...rest} component={Component}
            key={props.location.pathname + props.location.search} />;
    },
);

const makeRoute = () => { };

export { PublicRoute, PrivateRoute, makeRoute };

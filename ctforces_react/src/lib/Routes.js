import React from 'react';

import { Route, Redirect } from 'react-router-dom';
import withAuth from '../wrappers/withAuth';

const PrivateRoute = withAuth(
    ({ auth, component: Component, ...rest }) => {
        if (!auth.requested) {
            return null;
        }

        return (
            <Route
                {...rest}
                render={props => (auth.loggedIn ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                            pathname: '/login',
                            state: { from: props.location },
                        }}
                    />
                ))
                }
            />
        );
    },
    {
        request: true,
    },
);

const PublicRoute = withAuth(
    ({ auth, component: Component, ...rest }) => <Route {...rest} component={Component} />,
    {
        request: true,
    },
);

export { PublicRoute, PrivateRoute };

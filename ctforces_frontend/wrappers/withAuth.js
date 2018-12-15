import React, { Component } from 'react';
import { getUser, loggedIn } from '../lib/auth_service';
import redirect from '../lib/redirect';

export const AuthCtx = React.createContext(null);

export default function withAuth(AuthComponent, options) {
    return class Authenticated extends Component {
        state = { auth: { loggedIn: false, user: false } };

        constructor(props) {
            super(props);
        }

        updateAuth = user => {
            if (user) {
                this.setState({
                    auth: {
                        loggedIn: true,
                        user: user
                    }
                });
            } else {
                this.setState({
                    auth: {
                        loggedIn: false,
                        user: false
                    }
                });
            }
        };

        render() {
            return (
                <AuthCtx.Provider
                    value={{
                        auth: this.state.auth,
                        updateAuth: this.updateAuth
                    }}
                >
                    <AuthComponent {...this.props} />
                </AuthCtx.Provider>
            );
        }
    };
}

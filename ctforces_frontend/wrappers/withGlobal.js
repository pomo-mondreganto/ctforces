import React, { Component } from 'react';
import { getUser, loggedIn } from '../lib/auth_service';
import redirect from '../lib/redirect';

export const GlobalCtx = React.createContext(null);

export default function withGlobal(GlobalComponent, options) {
    return class Authenticated extends Component {
        state = {
            auth: { loggedIn: false, user: false },
            sidebars: { leftSidebar: false, rightSidebar: false }
        };

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

        updateSidebars = options => {
            if (options && options.leftSidebar !== undefined) {
                this.setState({
                    sidebars: {
                        leftSidebar: options.leftSidebar,
                        rightSidebar: this.state.sidebars.rightSidebar
                    }
                });
            }
            if (options && options.rightSidebar !== undefined) {
                this.setState({
                    sidebars: {
                        rightSidebar: options.rightSidebar,
                        leftSidebar: this.state.sidebars.leftSidebar
                    }
                });
            }
        };

        render() {
            return (
                <GlobalCtx.Provider
                    value={{
                        auth: this.state.auth,
                        updateAuth: this.updateAuth,
                        sidebars: this.state.sidebars,
                        updateSidebars: this.updateSidebars
                    }}
                >
                    <GlobalComponent {...this.props} />
                </GlobalCtx.Provider>
            );
        }
    };
}

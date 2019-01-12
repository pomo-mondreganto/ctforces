import React, { Component } from 'react';
import { getUser, loggedIn } from '../lib/auth_service';
import redirect from '../lib/redirect';

export const GlobalCtx = React.createContext(null);

export default function withGlobal(GlobalComponent, options) {
    return class Authenticated extends Component {
        constructor(props) {
            super(props);
            this.state = {
                auth: { loggedIn: false, user: false },
                sidebars: { leftSidebar: false, rightSidebar: false }
            };
        }

        static redirectToLogin(ctx) {
            if (ctx && ctx.res) {
                ctx.res.writeHead(302, {
                    Location: `login?next=${ctx.req.originalUrl}`
                });
                ctx.res.end();
            } else {
                Router.push(`login?next=${ctx.asPath}`);
            }
        }

        static async getInitialProps({ Component, router, ctx }) {
            let { isGuarded } = Component;

            let data = await getUser({ ctx: ctx });

            let user = false;

            if (data) {
                user = { loggedIn: true, user: data };
            } else {
                user = { loggedIn: false, user: false };
            }

            if (isGuarded && user.user === false) {
                this.redirectToLogin(ctx);
            }

            let pageProps = {};

            if (Component.getInitialProps) {
                pageProps = await Component.getInitialProps(ctx);
            }

            return { pageProps, initial_user: user, guarded: isGuarded };
        }

        updateAuth = user => {
            if (user) {
                this.setState({ auth: { loggedIn: true, user: user } });
            } else {
                this.setState({ auth: { loggedIn: false, user: false } });
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
                        updateSidebars: this.updateSidebars,
                        initial_user: this.props.initial_user,
                        guarded: this.props.guarded
                    }}
                >
                    <GlobalComponent {...this.props} />
                </GlobalCtx.Provider>
            );
        }
    };
}

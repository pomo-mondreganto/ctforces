import React, { Component } from 'react';
import { getUser } from '../lib/auth_service';
import redirect from '../lib/redirect';
import { GlobalCtx } from './withGlobal';

export default function withLayout(ChildComponent, LayoutComponent, options) {
    return class ComponentWithLayout extends Component {
        static contextType = GlobalCtx;
        state = { guarded: options && options.guarded };

        constructor(props) {
            super(props);
        }

        static async getInitialProps(ctx) {
            let pageProps = {};

            if (ChildComponent.getInitialProps) {
                pageProps = await ChildComponent.getInitialProps(ctx);
            }

            return pageProps;
        }

        componentDidMount = async () => {
            let data = await getUser();
            if (data) {
                this.context.updateAuth(data);
            } else {
                this.context.updateAuth(false);
                if (this.state.guarded) {
                    redirect('login');
                }
            }
        };

        render() {
            if (!this.state.guarded || this.context.auth.loggedIn) {
                return (
                    <LayoutComponent guarded={this.state.guarded}>
                        <ChildComponent {...this.props} />
                    </LayoutComponent>
                );
            } else {
                return <div />;
            }
        }
    };
}

import React, { Component } from 'react';
import { getUser } from '../lib/auth_service';
import redirect from '../lib/redirect';
import { AuthCtx } from './withAuth';

export default function withLayout(ChildComponent, LayoutComponent, options) {
    return class ComponentWithLayout extends Component {
        static contextType = AuthCtx;
        state = { guarded: options && options.guarded };

        constructor(props) {
            super(props);
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

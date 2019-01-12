import React, { Component } from 'react';
import { GlobalCtx } from '../wrappers/withGlobal';

export default function withAuth(ChildComponent) {
    return class AuthComponent extends Component {
        static contextType = GlobalCtx;

        constructor(props) {
            super(props);
            this.state = {
                user_updated: false
            };
        }

        static async getInitialProps(ctx) {
            let pageProps = {};

            if (ChildComponent.getInitialProps) {
                pageProps = await ChildComponent.getInitialProps(ctx);
            }

            return pageProps;
        }

        componentDidMount() {
            this.context.updateAuth(this.context.initial_user.user);
            this.setState({
                user_updated: true
            });
        }

        render() {
            return (
                <ChildComponent
                    auth={
                        this.state.user_updated
                            ? this.context.auth
                            : this.context.initial_user
                    }
                    updateAuth={this.context.updateAuth}
                    guarded={this.context.guarded}
                    {...this.props}
                />
            );
        }
    };
}

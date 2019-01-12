import React, { Component } from 'react';

export default function withGuard(ChildComponent) {
    return class GuardedComponent extends Component {
        static isGuarded = true;

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

        render() {
            return <ChildComponent {...this.props} />;
        }
    };
}

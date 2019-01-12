import React, { Component } from 'react';
import { getUser } from '../lib/auth_service';
import redirect from '../lib/redirect';
import { GlobalCtx } from './withGlobal';

export default function withLayout(ChildComponent, LayoutComponent, options) {
    return class ComponentWithLayout extends Component {
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
            return (
                <LayoutComponent>
                    <ChildComponent {...this.props} />
                </LayoutComponent>
            );
        }
    };
}

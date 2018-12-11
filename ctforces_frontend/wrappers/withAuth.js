import React, { Component } from 'react';
import { loggedIn } from '../lib/AuthService';
import Router from 'next/router';
import redirect from '../lib/redirect';

export default function withAuth(AuthComponent) {
    return class Authenticated extends Component {
        constructor(props) {
            super(props);
        }

        static getInitialProps = async ctx => {
            let isLoggedIn = await loggedIn();
            if (!isLoggedIn) {
                redirect('/login', ctx);
                return {};
            } else {
                let props = {};
                if (AuthComponent.getInitialProps) {
                    props = AuthComponent.getInitialProps(ctx);
                }
                return props;
            }
        };

        render() {
            return (
                <div>
                    <AuthComponent {...this.props} />
                </div>
            );
        }
    };
}

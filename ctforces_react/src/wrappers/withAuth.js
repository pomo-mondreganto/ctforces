import React from 'react';

import { Creators } from '../store/auth/actions';
import { connect } from 'react-redux';
import axios from 'axios';

export default (ChildComponent, options = { request: false }) => {
    const AuthComponent = class extends React.Component {
        constructor(props) {
            super(props);
        }

        async componentDidMount() {
            if (options.request) {
                try {
                    const response = await axios.get(`/me/`);
                    this.props.updateAuthUser({
                        loggedIn: true,
                        user: response.data,
                        requested: true
                    });
                } catch {
                    this.props.updateAuthUser({
                        loggedIn: false,
                        user: null,
                        requested: true
                    });
                }
            }
        }

        render() {
            return <ChildComponent {...this.props} />;
        }
    };

    const mapStateToProps = state => {
        return {
            auth: state.auth
        };
    };

    const mapDispatchToProps = {
        updateAuthUser: Creators.updateAuthUser
    };

    return connect(
        mapStateToProps,
        mapDispatchToProps
    )(AuthComponent);
};

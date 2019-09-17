import React from 'react';

import { connect } from 'react-redux';
import { Creators } from 'store/auth/actions';

export default (ChildComponent) => {
    const AuthComponent = class AuthComponentClass extends React.Component {
        render() {
            return <ChildComponent {...this.props} />;
        }
    };

    const mapStateToProps = state => ({
        auth: state.auth,
    });

    const mapDispatchToProps = {
        updateAuthUser: Creators.updateAuthUser,
    };

    return connect(
        mapStateToProps,
        mapDispatchToProps,
    )(AuthComponent);
};

import React from 'react';

import Component from './Component';
import axios from 'axios';

import withAuth from '../../wrappers/withAuth';

class MenuContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isOpen: false
        };
    }

    toggle = () => {
        this.setState({
            isOpen: !this.state.isOpen
        });
    };

    logout = async () => {
        try {
            const response = await axios.post(`/logout/`);
        } catch {}
        this.props.updateAuthUser({
            loggedIn: false,
            user: null,
            requested: true
        });
    };

    render() {
        return (
            <Component
                isOpen={this.state.isOpen}
                logout={this.logout}
                toggle={this.toggle}
                auth={this.props.auth}
            />
        );
    }
}

export default withAuth(MenuContainer);

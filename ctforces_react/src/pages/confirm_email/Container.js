import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';
import qs from 'lib/qs';
import Component from './Component';

class ConfirmEmailPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
            title: 'Redirecting...',
        };
    }

    async componentDidMount() {
        const { token = '' } = qs(this.props.location.search);
        try {
            await axios.post('/confirm_email/', {
                token,
            });
            this.setState({
                redirect: '/login/',
            });
        } catch (error) {
            this.setState({
                title: 'Incorrect token',
            });
        }
    }

    render() {
        if (this.state.redirect !== null) {
            return <Redirect to={this.state.redirect} />;
        }

        return <Component title={this.state.title} />;
    }
}

export default withAuth(ConfirmEmailPage);

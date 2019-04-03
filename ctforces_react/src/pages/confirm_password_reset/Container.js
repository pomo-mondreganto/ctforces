import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';
import qs from 'lib/qs';
import Component from './Component';

class ConfirmPasswordResetPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
            token: '',
        };
    }

    async componentDidMount() {
        const { token = '' } = qs(this.props.location.search);
        this.setState({ token });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            await axios.post('/reset_password/', values);
            if (this.props.auth.loggedIn) {
                this.setState({
                    redirect: '/',
                });
            } else {
                this.setState({
                    redirect: '/login/',
                });
            }
        } catch (error) {
            const errorData = error.response.data;
            Object.keys(errorData).forEach((key) => {
                actions.setFieldError(key, errorData[key]);
                actions.setFieldTouched(key, true, false);
            });
            actions.setSubmitting(false);
        }
    };

    render() {
        if (this.state.redirect !== null) {
            return <Redirect to={this.state.redirect} />;
        }

        return <Component handleSubmit={this.handleSubmit} token={this.state.token} />;
    }
}

export default withAuth(ConfirmPasswordResetPage);

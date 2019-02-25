import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Component from './Component';
import withAuth from '../../wrappers/withAuth';

class LoginPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
        };
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            const response = await axios.post('/login/', values);
            this.props.updateAuthUser({
                requested: true,
                user: response.data,
                loggedIn: true,
            });
            if (this.props.location.state && this.props.location.state.from) {
                this.setState({
                    redirect: this.props.location.state.from,
                });
            } else {
                this.setState({
                    redirect: '/',
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

        return <Component handleSubmit={this.handleSubmit} />;
    }
}

export default withAuth(LoginPage);

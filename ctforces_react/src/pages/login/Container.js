import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';
import qs from 'lib/qs';
import Component from './Component';

class LoginPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
        };
    }

    componentDidMount() {
        console.log('here');
        const { email_sent: emailSent } = qs(this.props.location.search);
        console.log(emailSent);
        this.setState({ emailSent });
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
            let needResend = false;
            Object.keys(errorData).forEach((key) => {
                actions.setFieldError(key, errorData[key]);
                actions.setFieldTouched(key, true, false);
                if (errorData[key] === 'User is not activated') {
                    needResend = true;
                }
            });
            actions.setSubmitting(false);
            this.setState({ needResend });
        }
    };

    render() {
        if (this.state.redirect !== null) {
            return <Redirect to={this.state.redirect} />;
        }

        return <Component
            handleSubmit={this.handleSubmit}
            needResend={this.state.needResend}
            emailSent={this.state.emailSent}
        />;
    }
}

export default withAuth(LoginPage);

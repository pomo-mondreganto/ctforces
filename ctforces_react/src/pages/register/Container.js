import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';
import Component from './Component';

class RegisterPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
        };
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            await axios.post('/register/', values);
            this.setState({
                redirect: '/login/?email_sent=1',
            });
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

export default withAuth(RegisterPage);

import React from 'react';

import Component from './Component';
import axios from 'axios';
import withAuth from '../../wrappers/withAuth';
import { Redirect } from 'react-router-dom';

class RegisterPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: false
        };
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            const response = await axios.post('/register/', values);
            this.setState({
                redirect: true
            });
        } catch (error) {
            const errorData = error.response.data;
            for (const key in errorData) {
                actions.setFieldError(key, errorData[key]);
                actions.setFieldTouched(key, true, false);
            }
            actions.setSubmitting(false);
        }
    };

    render() {
        if (this.state.redirect) {
            return <Redirect to="/login" />;
        }

        return <Component handleSubmit={this.handleSubmit} />;
    }
}

export default withAuth(RegisterPage);

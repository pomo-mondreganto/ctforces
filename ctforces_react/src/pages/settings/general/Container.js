import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import withAuth from 'wrappers/withAuth';
import Component from './Component';

class GeneralSettingsPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
        };
    }

    handleSubmit = async ({ values, actions }) => {
        const {
            old_password: oldPassword,
            password,
        } = values;
        try {
            await axios.put('/me/', {
                password,
                old_password: oldPassword,
            });
            this.setState({
                redirect: `/users/${this.props.auth.user.username}/`,
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

    handleSubmitAvatar = async ({ values, actions }) => {
        const {
            avatar,
        } = values;
        try {
            const formData = new FormData();

            const file = avatar[0];

            formData.append('avatar', file);

            const uploadingStatus = {};

            await axios.post('/avatar_upload/', formData, {
                onUploadProgress: (progressEvent) => {
                    uploadingStatus[file.name] = parseInt(
                        Math.round(
                            (progressEvent.loaded * 100)
                            / progressEvent.total,
                        ), 10,
                    );
                    actions.setStatus({
                        uploading: uploadingStatus,
                    });
                },
            });

            this.setState({
                redirect: `/users/${this.props.auth.user.username}`,
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

        return <Component handleSubmit={this.handleSubmit}
            handleSubmitAvatar={this.handleSubmitAvatar}
            auth={this.props.auth} />;
    }
}

export default withAuth(GeneralSettingsPage);

import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Component from './Component';

class TaskCreateContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
        };
    }

    handleTag = async (tag) => {
        const searchResponse = await axios.get('/task_tags/search/', {
            params: {
                name: tag,
            },
        });
        const tags = searchResponse.data;
        if (tags.length === 0 || tags[0].name !== tag) {
            const response = await axios.post('/task_tags/', {
                name: tag,
            });
            const newTag = response.data;
            return newTag.id;
        }
        return tags[0].id;
    };

    handleSubmit = async ({ values, actions }) => {
        try {
            const tagsNames = values.tags;
            const tags = [];
            for (let i = 0; i < tagsNames.length; i += 1) {
                const tag = tagsNames[i];
                tags.push(await this.handleTag(tag));
            }

            const uploadingStatus = {};
            const uploadPromises = [];
            for (let i = 0; i < values.files.length; i += 1) {
                const file = values.files[i];
                const formData = new FormData();
                formData.append('file_field', file);
                uploadPromises.push(
                    axios.post('/task_files/', formData, {
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
                    }),
                );
            }

            const data = await Promise.all(uploadPromises);
            actions.setStatus({});
            const files = [];
            for (let i = 0; i < values.files.length; i += 1) {
                files.push(data[i].data.id);
            }

            const response = await axios.post('/tasks/', {
                ...values,
                tags,
                files,
            });
            const { id } = response.data;
            this.setState({
                redirect: `/tasks/${id}`,
            });
        } catch (error) {
            const errorData = error.response.data;
            Object.keys(errorData).forEach((key) => {
                console.log(key);
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

export default TaskCreateContainer;

import React from 'react';

import axios from 'axios';
import { Redirect } from 'react-router-dom';
import Component from './Component';

class PostEditContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
            post: null,
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/posts/${id}/`);
        this.setState({
            post: response.data,
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            await axios.put(
                `/posts/${this.state.post.id}/`,
                values,
            );
            this.setState({
                redirect: `/posts/${this.state.post.id}/`,
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

        return (
            <Component
                handleSubmit={this.handleSubmit}
                post={this.state.post}
            />
        );
    }
}

export default PostEditContainer;

import React from 'react';

import Component from './Component';
import axios from 'axios';
import { Redirect } from 'react-router-dom';

class PostEditContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            redirect: null,
            post: null
        };
    }

    async componentDidMount() {
        const { id } = this.props.match.params;
        const response = await axios.get(`/posts/${id}/`);
        this.setState({
            post: response.data
        });
    }

    handleSubmit = async ({ values, actions }) => {
        try {
            const response = await axios.put(
                `/posts/${this.state.post.id}/`,
                values
            );
            this.setState({
                redirect: `/posts/${this.state.post.id}/`
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

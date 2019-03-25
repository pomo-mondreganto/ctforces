import React from 'react';

import axios from 'axios';
import Component from './Component';
import withAuth from '../../../wrappers/withAuth';

class UserIndexPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: null,
        };
    }

    async componentDidMount() {
        const { username } = this.props.match.params;
        const response = await axios.get(`/users/${username}/`);
        this.setState({
            user: response.data,
        });
    }

    render() {
        return (
            <Component
                user={this.state.user}
                auth={this.props.auth}
                username={this.props.match.params.username}
            />
        );
    }
}

export default withAuth(UserIndexPage);

import React from 'react';

import withAuth from 'wrappers/withAuth';
import axios from 'axios';
import Component from './Component';

class SidebarContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    async componentDidMount() {
        const response = await axios.get('/users/rating_top/');
        const { data } = response;
        const { results: users } = data;
        this.setState({
            users,
        });
    }

    render() {
        return <Component auth={this.props.auth} topUsers={this.state.users} />;
    }
}

export default withAuth(SidebarContainer);

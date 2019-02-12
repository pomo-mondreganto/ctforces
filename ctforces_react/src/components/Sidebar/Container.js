import React from 'react';

import Component from './Component';
import withAuth from '../../wrappers/withAuth';

class SidebarContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <Component auth={this.props.auth} />;
    }
}

export default withAuth(SidebarContainer);

import React from 'react';

import withAuth from 'wrappers/withAuth';
import Component from './Component';

class SidebarContainer extends React.Component {
    render() {
        return <Component auth={this.props.auth} />;
    }
}

export default withAuth(SidebarContainer);

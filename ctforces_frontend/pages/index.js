import sidebarLayout from '../layouts/sidebarLayout';
import React, { Component } from 'react';
import withLayout from '../wrappers/withLayout';

class Index extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <div />;
    }
}

export default withLayout(Index, sidebarLayout, {
    guarded: false
});

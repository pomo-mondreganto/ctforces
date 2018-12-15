import Layout from '../layouts/master.js';
import React, { Component } from 'react';
import withLayout from '../wrappers/withLayout';

class Index extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return <div>kek</div>;
    }
}

export default withLayout(Index, Layout, {
    guarded: true
});

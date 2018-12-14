import Layout from '../layouts/master.js';
import withAuth from '../wrappers/withAuth';
import React, {Component} from 'react';

class Index extends Component {
    constructor(props) {
        super(props);
    }

    render() {
      return <Layout/>;
    }
}

export default withAuth(Index);

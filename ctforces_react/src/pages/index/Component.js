import React from 'react';
import withLayout from '../../wrappers/withLayout';
import Layout from '../../layouts/master/Container';

const Component = props => {
    return <div>Hello</div>;
};

export default withLayout(Component, Layout);

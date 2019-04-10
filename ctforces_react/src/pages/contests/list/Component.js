import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import ContestView from 'components/Models/Contests/ContestView';

import 'styles/pages/contests.scss';

const Component = props => (
    <ContestView
        title="Contests"
        paginationUrl="/contests/"
        {...props}
    />
);

export default withLayout(Component, Layout);

import React from 'react';

import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import ContestView from 'components/Models/Contests/ContestView';
import UserTopBar from 'snippets_components/UserTopBar';

import 'styles/pages/contests.scss';

const Component = props => (
    <ContestView
        tabs={UserTopBar(props.username, props.auth)}
        paginationUrl={`/users/${props.username}/contests/`}
        {...props}
    />
);

export default withLayout(Component, Layout);

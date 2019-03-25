import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';
import Pagination from 'components/Pagination/Container';
import withLayout from '../../../wrappers/withLayout';
import Layout from '../../../layouts/sidebar/Container';
import CardWithTabsComponent from '../../../components/CardWithTabs/Container';

import '../styles.scss';

const Component = props => (
    <CardWithTabsComponent
        tabs={[
            {
                text: props.username,
                href: `/users/${props.username}`,
            },
            { text: 'Blog', href: `/users/${props.username}/posts/` },
            { text: 'Tasks', href: `/users/${props.username}/tasks/` },
            { text: 'General', href: '/settings/general/' },
            { text: 'Social', href: '/settings/social/' },
        ]}
    >
        <>
            {props.tasks && props.tasks.map((obj, i) => (
                <div key={i}>
                    <LinkContainerNonActive to={`/users/${props.username}/tasks/${obj.id}/`}>
                        <a>
                            {obj.name}
                        </a>
                    </LinkContainerNonActive>
                </div>
            ))}
            {props.tasks
                && <Pagination to={`/users/${props.username}/tasks/`}
                    currentPage={props.currentPage}
                    count={props.count}
                    pageSize={props.pageSize} />}
        </>
    </CardWithTabsComponent>
);

export default withLayout(Component, Layout);

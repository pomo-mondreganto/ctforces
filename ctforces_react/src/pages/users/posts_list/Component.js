import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';
import Pagination from 'components/Pagination/Container';
import withLayout from 'wrappers/withLayout';
import Layout from 'layouts/sidebar/Container';
import CardWithTabsComponent from 'components/CardWithTabs/Container';

import 'styles/pages/users.scss';

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
            {props.posts && props.posts.map((obj, i) => (
                <div key={i}>
                    <div className="py-2">
                        <span style={{ fontSize: '2rem' }}>
                            <LinkContainerNonActive to={`/posts/${obj.id}/`}>
                                <a>{obj.title}</a>
                            </LinkContainerNonActive>
                            {' by '}
                            <LinkContainerNonActive to={`/users/${obj.author_username}/`} >
                                <a>{obj.author_username}</a>
                            </LinkContainerNonActive>
                        </span>
                    </div>
                    <hr />
                    <div className="py-2">
                        {' '}
                        <span style={{ fontSize: '2rem' }}>{obj.body}</span>
                    </div>
                </div>
            ))}
            {props.posts
                && <Pagination to={`/users/${props.username}/posts/`}
                    currentPage={props.currentPage}
                    count={props.count}
                    pageSize={props.pageSize} />}
        </>
    </CardWithTabsComponent>
);

export default withLayout(Component, Layout);

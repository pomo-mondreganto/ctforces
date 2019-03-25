import React from 'react';

import { LinkContainerNonActive } from 'lib/LinkContainer';
import withLayout from '../../../wrappers/withLayout';
import Layout from '../../../layouts/sidebar/Container';
import { mediaUrl } from '../../../../config/config';
import CardWithTabsComponent from '../../../components/CardWithTabs/Container';

import '../styles.scss';

const Component = props => (
    <CardWithTabsComponent
        tabs={[
            {
                text: props.username,
                href: `/users/${props.username}/`,
            },
            { text: 'Blog', href: `/users/${props.username}/posts/` },
            { text: 'Tasks', href: `/users/${props.username}/tasks/` },
            { text: 'General', href: '/settings/general/' },
            { text: 'Social', href: '/settings/social/' },
        ]}
    >
        {props.user !== null && (
            <section id="profile">
                <article id="info">
                    <div>
                        <span>Master</span>
                    </div>
                    {props.user.hide_personal_info || (
                        <span
                            style={{ fontSize: '1.5rem' }}
                            className="py-1"
                        >
                            {props.user.personal_info.first_name}{' '}
                            {props.user.personal_info.last_name}
                        </span>
                    )}
                    <div>
                        <span style={{ fontSize: '2rem' }} className="py-2">
                            {props.user.username}
                        </span>
                    </div>
                    <div className="py-2">
                        <span>Rating: {props.user.rating}</span>
                    </div>
                    <div className="py-2">
                        <span>Maximum rating: {props.user.max_rating}</span>
                    </div>
                    {props.auth.loggedIn
                        && props.auth.user.username === props.user.username && (
                        <div className="py-2">
                            <LinkContainerNonActive to="/posts/create/">
                                <a>Write post</a>
                            </LinkContainerNonActive>
                        </div>
                    )}
                    {props.auth.loggedIn
                        && props.auth.user.username === props.user.username && (
                        <div className="py-2">
                            <LinkContainerNonActive to="/tasks/create/">
                                <a>Create task</a>
                            </LinkContainerNonActive>
                        </div>
                    )}
                    {props.auth.loggedIn
                        && props.auth.user.username === props.user.username && (
                        <div className="py-2">
                            <LinkContainerNonActive to="/contests/create/">
                                <a>Create contest</a>
                            </LinkContainerNonActive>
                        </div>
                    )}
                </article>
                <article id="avatar">
                    <div>
                        <img
                            src={`${mediaUrl}${props.user.avatar_main}`}
                            className="img-fluid"
                        />
                    </div>
                </article>
            </section>
        )}
    </CardWithTabsComponent>
);

export default withLayout(Component, Layout);

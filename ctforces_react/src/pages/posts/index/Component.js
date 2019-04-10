import React from 'react';

import getRank from 'lib/ranking';
import convert from 'lib/HumanTime';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import Markdown from 'components/Markdown/Container';

import CardWithTabs from 'components/CardWithTabs/Container';

const Component = ({ post }) => (
    <CardWithTabs>
        {post !== null && (
            <>
                <div className="th1">
                    {post.title}
                </div>
                <div className="mt-3">
                    By {' '}
                    <LinkContainerNonActive to={`/users/${post.author_username}/`} >
                        <a className={getRank(post.author_rating)}>
                            {post.author_username}
                        </a>
                    </LinkContainerNonActive>
                    , {convert(post.created_at)}
                    {' '}
                    {post.can_edit_post && (
                        <>
                            {' '}
                            <LinkContainerNonActive
                                to={`/posts/${post.id}/edit/`}
                            >
                                <FontAwesomeIcon icon={faEdit} className="c-p" />
                            </LinkContainerNonActive>
                        </>
                    )}
                </div>

                <hr />
                <div className="py-2 long-text">
                    <Markdown text={post.body} />
                </div>
            </>
        )}

    </CardWithTabs>
);

export default withLayout(Component, Layout);

import React from 'react';

import { Card } from 'reactstrap';
import { LinkContainerNonActive } from '../../../lib/LinkContainer';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';

const Component = ({ post }) => {
    return (
        <Card className="p-2">
            {post !== null && (
                <>
                    <div className="py-2">
                        <span style={{ fontSize: '2rem' }}>
                            {post.title + ' by ' + post.author_username}
                        </span>
                    </div>
                    {post.can_edit_post && (
                        <div className="py-2">
                            <LinkContainerNonActive
                                to={`/posts/${post.id}/edit`}
                            >
                                <a>Edit post</a>
                            </LinkContainerNonActive>
                        </div>
                    )}
                    <hr />
                    <div className="py-2">
                        {' '}
                        <span style={{ fontSize: '2rem' }}>{post.body}</span>
                    </div>
                </>
            )}
        </Card>
    );
};

export default withLayout(Component, Layout);

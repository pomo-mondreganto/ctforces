import React from 'react';

import {
    Card, CardBody, CardSubtitle, CardText, CardTitle,
} from 'reactstrap';
import { getRank, getRankColor } from 'lib/Ranking';
import moment from 'moment';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

const Component = ({ post }) => (
    <Card className="p-2">
        {post !== null && (
            <CardBody>
                <CardTitle>
                    <p className="h2">{post.title}</p>
                </CardTitle>
                <CardSubtitle>
                    By <span style={{
                        color: getRankColor(getRank(post.author_rating)),
                    }}>
                        <LinkContainerNonActive
                            to={`/users/${post.author_username}/`}
                        >
                            <span>
                                {post.author_username}
                            </span>
                        </LinkContainerNonActive>
                    </span>, {' '}
                    {moment(post.created_at).format('LLL')}
                    {'  '}
                    {post.can_edit_post && (
                        <LinkContainerNonActive
                            to={`/posts/${post.id}/edit/`}
                        >
                            <FontAwesomeIcon icon={faEdit} />
                        </LinkContainerNonActive>
                    )}
                </CardSubtitle>
                <hr />
                <CardText>
                    {post.body}
                </CardText>
            </CardBody>
        )}

    </Card>
);

export default withLayout(Component, Layout);

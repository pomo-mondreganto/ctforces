import React from 'react';

import { Card, Row, Col } from 'reactstrap';
import withLayout from '../../../wrappers/withLayout';
import Layout from '../../../layouts/sidebar/Container';
import { LinkContainer } from 'react-router-bootstrap';
import { media_url } from '../../../../config/config';
import CardWithTabsComponent from '../../../components/CardWithTabs/Container';

const Component = props => {
    return (
        <CardWithTabsComponent
            tabs={[
                {
                    text: props.username,
                    href: `/users/${props.username}`
                },
                { text: 'Blog', href: `/users/${props.username}/posts` },
                { text: 'Tasks', href: `/users/${props.username}/tasks` },
                { text: 'General', href: '/settings/general' },
                { text: 'Social', href: '/settings/social' }
            ]}
        >
            {props.user !== null && (
                <Row>
                    <Col className="col-8 m-2">
                        <div>Master</div>
                        {props.user.hide_personal_info || (
                            <div
                                style={{ fontSize: '1.5rem' }}
                                className="py-1"
                            >
                                {props.user.personal_info.first_name}{' '}
                                {props.user.personal_info.last_name}
                            </div>
                        )}
                        <div style={{ fontSize: '2rem' }} className="py-2">
                            {props.user.username}
                        </div>
                        <div className="py-2">Rating: {props.user.rating}</div>
                        <div className="py-2">
                            Maximum rating: {props.user.max_rating}
                        </div>
                        {props.auth.loggedIn &&
                            props.auth.user.username == props.user.username && (
                                <div className="py-2">
                                    <LinkContainer to="/posts/create">
                                        <a>Write post</a>
                                    </LinkContainer>
                                </div>
                            )}
                        {props.auth.loggedIn &&
                            props.auth.user.username == props.user.username && (
                                <div className="py-2">
                                    <LinkContainer to="/task/create">
                                        <a>Create task</a>
                                    </LinkContainer>
                                </div>
                            )}
                        {props.auth.loggedIn &&
                            props.auth.user.username == props.user.username && (
                                <div className="py-2">
                                    <LinkContainer to="/contest/create">
                                        <a>Create contest</a>
                                    </LinkContainer>
                                </div>
                            )}
                    </Col>
                    <Col>
                        <img
                            src={`${media_url}${props.user.avatar_main}`}
                            className="img-fluid"
                        />
                    </Col>
                </Row>
            )}
        </CardWithTabsComponent>
    );
};

export default withLayout(Component, Layout);

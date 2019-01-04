import React, { Component } from 'react';
import sidebarLayout from '../layouts/sidebarLayout';
import withLayout from '../wrappers/withLayout';
import CardWithTabsComponent from '../components/CardWithTabs';
import { GlobalCtx } from '../wrappers/withGlobal';
import { media_url } from '../config';
import Link from 'next/link';

import { Card, Row, Col } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';

class Profile extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <CardWithTabsComponent
                    tabs={[
                        {
                            text: this.context.auth.user.username,
                            href: `/users/${this.context.auth.user.username}`
                        },
                        { text: 'Blog', href: '#' },
                        { text: 'Tasks', href: '#' },
                        { text: 'General', href: '/settings/general' },
                        { text: 'Social', href: '/settings/social' }
                    ]}
                >
                    <Row>
                        <Col className="col-8 m-2">
                            <div>Master</div>
                            {this.context.auth.user.hide_personal_info || (
                                <div
                                    style={{ fontSize: '1.5rem' }}
                                    className="py-1"
                                >
                                    {
                                        this.context.auth.user.personal_info
                                            .first_name
                                    }{' '}
                                    {
                                        this.context.auth.user.personal_info
                                            .last_name
                                    }
                                </div>
                            )}
                            <div style={{ fontSize: '2rem' }} className="py-2">
                                {this.context.auth.user.username}
                            </div>
                            <div className="py-2">
                                <FontAwesomeIcon icon={faChartLine} size="lg" />{' '}
                                Rating: {this.context.auth.user.rating}
                            </div>
                            <div className="py-2">
                                <FontAwesomeIcon icon={faChartLine} size="lg" />{' '}
                                Maximum rating:{' '}
                                {this.context.auth.user.max_rating}
                            </div>
                            <div className="py-2">
                                <FontAwesomeIcon icon={faMarker} size="lg" />{' '}
                                <Link href="/post/create">
                                    <a>Write post</a>
                                </Link>
                            </div>
                        </Col>
                        <Col>
                            <img
                                src={
                                    media_url +
                                    this.context.auth.user.avatar_main
                                }
                                className="img-fluid"
                            />
                        </Col>
                    </Row>
                </CardWithTabsComponent>
            </div>
        );
    }
}

export default withLayout(Profile, sidebarLayout, {
    guarded: true
});

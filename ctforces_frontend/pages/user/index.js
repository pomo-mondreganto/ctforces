import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import { get } from '../../lib/api_requests';
import { withRouter } from 'next/router';
import CardWithTabsComponent from '../../components/CardWithTabs';
import { media_url } from '../../config';
import { Link } from '../../server/routes';
import { GlobalCtx } from '../../wrappers/withGlobal';
import withAuth from '../../wrappers/withAuth';

import { Card, Row, Col } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';

class UserProfile extends Component {
    constructor(props) {
        super(props);
    }

    static async getInitialProps(ctx) {
        let data = await get(`users/${ctx.query.username}`, {
            ctx: ctx
        });
        return {
            user: await data.json()
        };
    }

    render() {
        return (
            <div>
                <CardWithTabsComponent
                    tabs={[
                        {
                            text: this.props.user.username,
                            href: `/user/${this.props.user.username}`
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
                            {this.props.user.hide_personal_info || (
                                <div
                                    style={{ fontSize: '1.5rem' }}
                                    className="py-1"
                                >
                                    {this.props.user.personal_info.first_name}{' '}
                                    {this.props.user.personal_info.last_name}
                                </div>
                            )}
                            <div style={{ fontSize: '2rem' }} className="py-2">
                                {this.props.user.username}
                            </div>
                            <div className="py-2">
                                <FontAwesomeIcon icon={faChartLine} size="lg" />{' '}
                                Rating: {this.props.user.rating}
                            </div>
                            <div className="py-2">
                                <FontAwesomeIcon icon={faChartLine} size="lg" />{' '}
                                Maximum rating: {this.props.user.max_rating}
                            </div>
                            {this.props.auth.loggedIn &&
                                this.props.auth.user.username ==
                                    this.props.user.username && (
                                    <div className="py-2">
                                        <FontAwesomeIcon
                                            icon={faMarker}
                                            size="lg"
                                        />{' '}
                                        <Link route="/post/create">
                                            <a>Write post</a>
                                        </Link>
                                    </div>
                                )}
                            {this.props.auth.loggedIn &&
                                this.props.auth.user.username ==
                                    this.props.user.username && (
                                    <div className="py-2">
                                        <FontAwesomeIcon
                                            icon={faMarker}
                                            size="lg"
                                        />{' '}
                                        <Link route="/task/create">
                                            <a>Create task</a>
                                        </Link>
                                    </div>
                                )}
                        </Col>
                        <Col>
                            <img
                                src={media_url + this.props.user.avatar_main}
                                className="img-fluid"
                            />
                        </Col>
                    </Row>
                </CardWithTabsComponent>
            </div>
        );
    }
}

export default withAuth(withLayout(UserProfile, sidebarLayout));

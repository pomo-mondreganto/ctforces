import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import CardWithTabsComponent from '../../components/CardWithTabs';
import { GlobalCtx } from '../../wrappers/withGlobal';
import { media_url } from '../../config';
import FormComponent from '../../components/Form';
import withAuth from '../wrappers/withAuth';

import { Card, Row, Col } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';
import FileUploaderComponent from '../../components/FileUploaderInput';

class SettingsSocial extends Component {
    constructor(props) {
        super(props);
    }

    onOkSubmit = () => {};

    render() {
        return (
            <div>
                <CardWithTabsComponent
                    tabs={[
                        {
                            text: this.props.auth.user.username,
                            href: `/user/${this.props.auth.user.username}`
                        },
                        { text: 'Blog', href: '#' },
                        { text: 'Tasks', href: '#' },
                        { text: 'General', href: '/settings/general' },
                        { text: 'Social', href: '/settings/social' }
                    ]}
                >
                    <Row>
                        <Col>
                            <FormComponent
                                onOkSubmit={this.onOkSubmit}
                                fields={[
                                    {
                                        source: FileUploaderComponent,
                                        name: 'avatar'
                                    }
                                ]}
                            />
                        </Col>
                    </Row>
                </CardWithTabsComponent>
            </div>
        );
    }
}

export default withAuth(withLayout(SettingsSocial, sidebarLayout));

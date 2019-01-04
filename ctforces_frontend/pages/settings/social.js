import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import CardWithTabsComponent from '../../components/CardWithTabs';
import { GlobalCtx } from '../../wrappers/withGlobal';
import { media_url } from '../../config';
import Link from 'next/link';
import FileUploadComponent from '../../components/FileUploader';

import { Card, Row, Col } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';

class SettingsSocial extends Component {
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
                            href: '/users/' + this.context.auth.user.username
                        },
                        { text: 'Blog', href: '#' },
                        { text: 'Tasks', href: '#' },
                        { text: 'General', href: '/settings/general' },
                        { text: 'Social', href: '/settings/social' }
                    ]}
                >
                    <Row>
                        <Col>
                            <FileUploadComponent />
                        </Col>
                    </Row>
                </CardWithTabsComponent>
            </div>
        );
    }
}

export default withLayout(SettingsSocial, sidebarLayout, {
    guarded: true
});

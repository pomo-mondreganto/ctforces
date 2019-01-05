import React, { Component } from 'react';
import sidebarLayout from '../../layouts/sidebarLayout';
import withLayout from '../../wrappers/withLayout';
import CardWithTabsComponent from '../../components/CardWithTabs';
import { GlobalCtx } from '../../wrappers/withGlobal';
import { media_url } from '../../config';
import Link from 'next/link';
import FormComponent from '../../components/Form';

import { Card, Row, Col } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChartLine, faMarker } from '@fortawesome/free-solid-svg-icons';
import FileUploaderComponent from '../../components/FileUploaderInput';

class SettingsSocial extends Component {
    static contextType = GlobalCtx;

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
                            text: this.context.auth.user.username,
                            as: `/user/${this.context.auth.user.username}`,
                            href: `/user?username=${
                                this.context.auth.user.username
                            }`
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

export default withLayout(SettingsSocial, sidebarLayout, {
    guarded: true
});

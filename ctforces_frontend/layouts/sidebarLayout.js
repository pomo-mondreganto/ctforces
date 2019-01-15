import Layout from './master';
import React, { Component } from 'react';
import { GlobalCtx } from '../wrappers/withGlobal';
import SidebarComponent from '../components/Sidebar';

import { Col, Row } from 'reactstrap';

class sidebarLayout extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Layout>
                <Row>
                    <Col>{this.props.children}</Col>
                    <Col className="overflow-hidden col-4">
                        <SidebarComponent />
                    </Col>
                </Row>
            </Layout>
        );
    }
}

export default sidebarLayout;

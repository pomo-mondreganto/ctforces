import Layout from './master';
import React, { Component } from 'react';
import { GlobalCtx } from '../wrappers/withGlobal';
import SidebarComponent from '../components/Sidebar';
import 'bootstrap/dist/css/bootstrap.css';

import { Col, Row } from 'reactstrap';

class sidebarLayout extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Layout guarded={this.props.guarded}>
                <Row>
                    <Col>{this.props.children}</Col>
                    <Col xs={3} className="overflow-hidden">
                        <SidebarComponent />
                    </Col>
                </Row>
            </Layout>
        );
    }
}

export default sidebarLayout;

import Layout from './master';
import React, { Component } from 'react';
import withLayout from '../wrappers/withLayout';
import classNames from 'classnames';
import { GlobalCtx } from '../wrappers/withGlobal';
import Sidebar from '../components/Sidebar';

import { Row, Col, Button } from 'reactstrap';

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
                    <Col className="col-3">
                        <Sidebar />
                    </Col>
                </Row>
            </Layout>
        );
    }
}

export default sidebarLayout;

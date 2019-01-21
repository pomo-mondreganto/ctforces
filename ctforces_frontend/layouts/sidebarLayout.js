import Layout from './master';
import React, {Component} from 'react';
import {GlobalCtx} from '../wrappers/withGlobal';
import SidebarComponent from '../components/Sidebar';

import {Col, Row} from 'reactstrap';

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
                    <Col
                        className={"overflow-hidden " + (!this.context.sidebars.rightSidebar ? "d-none" : "") + " d-lg-inline-block d-xl-inline col-lg-4 col-xl-4"}>
                        <SidebarComponent />
                    </Col>
                </Row>
            </Layout>
        );
    }
}

export default sidebarLayout;

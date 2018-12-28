import Layout from './master';
import React, { Component } from 'react';
import withLayout from '../wrappers/withLayout';
import classNames from 'classnames';

import { Row, Col, Button } from 'reactstrap';
import { CSSTransition } from 'react-transition-group';

import { isMobile } from 'react-device-detect';

class sidebarLayout extends Component {
    state = { sidebarActive: !isMobile };

    constructor(props) {
        super(props);
    }

    hideSidebar = () => {
        this.setState({ sidebarActive: !this.state.sidebarActive });
    };

    render() {
        return (
            <Layout guarded={this.props.guarded}>
                <Row>
                    <Col>{this.props.children}</Col>
                    <Col className="col-3">
                        <div />
                        <CSSTransition
                            in={this.state.sidebarActive}
                            timeout={300}
                            classNames="sidebar-right"
                            unmountOnExit
                        >
                            <nav className="sidebar-right">kke</nav>
                        </CSSTransition>
                    </Col>
                </Row>
                <Button onClick={this.hideSidebar} />
                <style jsx>{`
                    .sidebar-right {
                        float: right;
                        min-width: 100%;
                        background-color: blue;
                    }
                    .sidebar-right-exit {
                        margin-right: 0;
                    }
                    .sidebar-right-exit-active {
                        margin-right: -110%;
                        transition: all 0.3s linear;
                    }
                    .sidebar-right-enter {
                        margin-right: -110%;
                    }
                    .sidebar-right-enter-active {
                        margin-right: 0;
                        transition: all 0.3s linear;
                    }
                `}</style>
            </Layout>
        );
    }
}

export default sidebarLayout;

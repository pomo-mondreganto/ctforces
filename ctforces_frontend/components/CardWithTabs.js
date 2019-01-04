import React, { Component } from 'react';
import Link from 'next/link';

import { Col, Container, Nav, NavItem, NavLink, Row } from 'reactstrap';

class CardWithTabsComponent extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Container>
                <Row>
                    <Col>
                        <Nav className="nav-tabs nav-fill">
                            {this.props.tabs.map((obj, i) => {
                                return (
                                    <NavItem key={i}>
                                        <Link href={obj.href} href>
                                            <NavLink active={i === 0}>
                                                {obj.text}
                                            </NavLink>
                                        </Link>
                                    </NavItem>
                                );
                            })}
                        </Nav>
                    </Col>
                </Row>
                <Row className="p-2">
                    <Col>{this.props.children}</Col>
                </Row>
            </Container>
        );
    }
}

export default CardWithTabsComponent;

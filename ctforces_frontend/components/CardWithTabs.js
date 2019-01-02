import React, { Component } from 'react';
import Link from 'next/link';

import { Card, Nav, NavItem, NavLink } from 'reactstrap';

class CardWithTabsComponent extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Nav className="nav-pills nav-fill">
                    {this.props.tabs.map((obj, i) => {
                        return (
                            <NavItem key={i}>
                                <Link href={obj.href} passHref>
                                    <NavLink className="border">
                                        {obj.text}
                                    </NavLink>
                                </Link>
                            </NavItem>
                        );
                    })}
                </Nav>
                <Card className="p-2">{this.props.children}</Card>
            </div>
        );
    }
}

export default CardWithTabsComponent;

import React, {Component} from 'react';
import {Link} from '../server/routes';
import {Container, Nav, NavItem, NavLink} from 'reactstrap';


class CardWithTabsComponent extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Container>
                <Nav className="nav-tabs nav-fill">
                    {this.props.tabs.map((obj, i) => {
                        return (
                            <NavItem key={i}>
                                <Link route={obj.href} passHref>
                                    <NavLink active={obj.active}>
                                        {obj.text}
                                    </NavLink>
                                </Link>
                            </NavItem>
                        );
                    })}
                </Nav>
                <div className="p-4 border-left border-right border-bottom rounded-bottom">
                    {this.props.children}
                </div>
            </Container>
        )
            ;
    }
}

export default CardWithTabsComponent;

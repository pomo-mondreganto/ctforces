import React from 'react';

import { Nav, NavItem, NavLink } from 'reactstrap';
import { LinkContainerAuto } from 'lib/LinkContainer';

const Component = (props) => {
    if (!props.tabs) {
        return null;
    }

    return (
        <nav>
            <Nav className="nav-tabs nav-fill">
                {props.tabs.map((obj, i) => (
                    <NavItem key={i}>
                        <LinkContainerAuto to={obj.href}>
                            <NavLink>{obj.text}</NavLink>
                        </LinkContainerAuto>
                    </NavItem>
                ))}
            </Nav>
            <div className="p-4 border-left border-right border-bottom rounded-bottom">
                {props.children}
            </div>
        </nav>
    );
};

export default Component;

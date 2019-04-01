import React from 'react';

import {
    Nav, NavItem, NavLink,
} from 'reactstrap';
import { LinkContainerAuto } from 'lib/LinkContainer';

import 'styles/components/Card.scss';

const Component = props => (
    <>
        {props.tabs && (
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
            </nav>
        )}
        <div className={`p-4 border-left border-right border-bottom rounded-top ${props.tabs ? '' : 'border-top'}`}>
            {props.title && (
                <p className="th1 ta-c mb-4">
                    {props.title}
                </p>
            )}
            {props.children}
        </div>
        {props.pagination && (
            <div className="p-4 border-left border-right border-bottom rounded-bottom card-tabs-footer">
                {props.pagination}
            </div>
        )}
    </>
);

export default Component;

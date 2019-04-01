import React from 'react';

import {
    Button,
    Collapse,
    Nav,
    Navbar,
    NavbarBrand,
    NavbarToggler,
    NavItem,
    NavLink,
} from 'reactstrap';
import {
    LinkContainerNonActive,
    LinkContainerAuto,
} from 'lib/LinkContainer';


const LoginButton = (props) => {
    if (!props.auth.requested) {
        return null;
    }

    if (props.auth.loggedIn) {
        return (
            <LinkContainerNonActive to={`/users/${props.auth.user.username}/`}>
                <Button color="primary" className="btn-block">
                    {props.auth.user.username}
                </Button>
            </LinkContainerNonActive>
        );
    }
    return (
        <LinkContainerNonActive to="/login/">
            <Button color="primary" className="btn-block">
                Login
            </Button>
        </LinkContainerNonActive>
    );
};

const RegisterButton = (props) => {
    if (!props.auth.requested) {
        return null;
    }

    if (props.auth.loggedIn) {
        return (
            <Button className="btn-block" onClick={props.onClick}>
                Logout
            </Button>
        );
    }
    return (
        <LinkContainerNonActive to="/register/">
            <Button className="btn-block">Register</Button>
        </LinkContainerNonActive>
    );
};

const Component = props => (
    <Navbar color="light" light expand="lg" className="shadow-sm">
        <NavbarToggler onClick={props.toggle} className="border-0">
            Menu
        </NavbarToggler>
        <LinkContainerNonActive to="/">
            <NavbarBrand className="d-xs-none d-sm-inline-block d-md-inline-block d-lg-inline-block d-xl-inline-block navbar-brand">
                CTForces
            </NavbarBrand>
        </LinkContainerNonActive>
        <NavbarToggler onClick={props.toggleSidebar} className="border-0">
            icon
        </NavbarToggler>
        <Collapse isOpen={props.isOpen} navbar>
            <Nav navbar className="w-100 pull-left nav-fill mr-auto">
                <NavItem>
                    <LinkContainerAuto to="/">
                        <NavLink>Home</NavLink>
                    </LinkContainerAuto>
                </NavItem>
                <NavItem>
                    <LinkContainerAuto to="/contests/">
                        <NavLink>Contests</NavLink>
                    </LinkContainerAuto>
                </NavItem>
                <NavItem>
                    <LinkContainerAuto to="/tasks/">
                        <NavLink>Tasks</NavLink>
                    </LinkContainerAuto>
                </NavItem>
                <NavItem>
                    <LinkContainerAuto to="/users/upsolving/top/">
                        <NavLink>Upsolving</NavLink>
                    </LinkContainerAuto>
                </NavItem>
                <NavItem>
                    <LinkContainerAuto to="/users/rating/top/">
                        <NavLink>Rating</NavLink>
                    </LinkContainerAuto>
                </NavItem>
            </Nav>
        </Collapse>

        <Collapse
            isOpen={props.isOpen}
            navbar
            className="justify-content-end mr-auto ml-auto w-25"
        >
            <Nav className="nav-fill" navbar>
                <NavItem className="mx-1 my-1">
                    <LoginButton auth={props.auth} />
                </NavItem>
                <NavItem className="mx-1 my-1">
                    <RegisterButton
                        auth={props.auth}
                        onClick={props.logout}
                    />
                </NavItem>
            </Nav>
        </Collapse>
    </Navbar>
);

export default Component;

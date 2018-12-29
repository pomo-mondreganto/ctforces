import React, { Component } from 'react';
import Link from 'next/link';
import { logout } from '../lib/auth_service';
import { GlobalCtx } from '../wrappers/withGlobal';
import redirect from '../lib/redirect';

import {
    Button,
    Collapse,
    Nav,
    Navbar,
    NavbarBrand,
    NavbarToggler,
    NavItem,
    NavLink
} from 'reactstrap';

function LoginButton(props) {
    if (props.authProp.auth.loggedIn) {
        return (
            <Link href="profile">
                <Button color="primary" className="btn-block">
                    {props.authProp.auth.user.username}
                </Button>
            </Link>
        );
    } else {
        return (
            <Link href="login">
                <Button color="primary" className="btn-block">
                    Sign In
                </Button>
            </Link>
        );
    }
}

function RegisterButton(props) {
    if (props.authProp.auth.loggedIn) {
        return (
            <Button className="btn-block" onClick={props.onClick}>
                Logout
            </Button>
        );
    } else {
        return (
            <Link href="register">
                <Button className="btn-block">Sign Up</Button>
            </Link>
        );
    }
}

class Menu extends Component {
    static contextType = GlobalCtx;

    constructor(props) {
        super(props);
        this.state = {
            isOpen: false
        };
    }

    hideSidebar = () => {
        this.context.updateSidebars({
            rightSidebar: !this.context.sidebars.rightSidebar
        });
    };

    toggle = () => {
        this.setState({
            isOpen: !this.state.isOpen
        });
    };

    logout = async () => {
        let data = await logout();
        this.context.updateAuth(false);
        if (this.props.guarded) {
            redirect('login');
        }
    };

    render() {
        return (
            <Navbar
                color="light"
                light
                sticky="top"
                expand="md"
                className="shadow-sm"
            >
                <NavbarToggler onClick={this.toggle} />
                <Collapse isOpen={this.state.isOpen} navbar>
                    <Link href="/">
                        <NavbarBrand
                            href="/"
                            className="d-xs-none d-sm-none d-md-inline-block d-lg-inline-block d-xl-inline-block navbar-brand"
                        >
                            CTForces
                        </NavbarBrand>
                    </Link>
                    <Nav navbar className="w-100 nav-fill mr-auto">
                        <NavItem>
                            <Link href="/">
                                <NavLink href="/">Home</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link href="/">
                                <NavLink href="/">Contests</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link href="/">
                                <NavLink href="/">Tasks</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link href="/">
                                <NavLink href="/">Upsolving</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link href="/">
                                <NavLink href="/">Rating</NavLink>
                            </Link>
                        </NavItem>
                    </Nav>
                </Collapse>

                <Collapse
                    isOpen={this.state.isOpen}
                    navbar
                    className="justify-content-end mr-auto ml-auto w-25"
                >
                    <Nav className="nav-fill" navbar>
                        <NavItem className="mx-1 my-1">
                            <Button
                                onClick={this.hideSidebar}
                                color="primary"
                                className="btn-block"
                            >
                                Toggle sidebar
                            </Button>
                        </NavItem>
                        <NavItem className="mx-1 my-1">
                            <LoginButton authProp={this.context} />
                        </NavItem>
                        <NavItem className="mx-1 my-1">
                            <RegisterButton
                                authProp={this.context}
                                onClick={this.logout}
                            />
                        </NavItem>
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }
}

export default Menu;

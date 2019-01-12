import React, { Component } from 'react';
import { Link } from '../server/routes';
import { logout } from '../lib/auth_service';
import { GlobalCtx } from '../wrappers/withGlobal';
import withAuth from '../wrappers/withAuth';
import redirect from '../lib/redirect';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars } from '@fortawesome/free-solid-svg-icons';

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
            <Link route={`/user/${props.authProp.auth.user.username}`}>
                <Button color="primary" className="btn-block">
                    {props.authProp.auth.user.username}
                </Button>
            </Link>
        );
    } else {
        return (
            <Link route="/login">
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
            <Link route="/register">
                <Button className="btn-block">Sign Up</Button>
            </Link>
        );
    }
}

class MenuComponent extends Component {
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
        this.props.updateAuth(false);
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
                expand="lg"
                className="shadow-sm"
            >
                <NavbarToggler onClick={this.toggle} className="border-0">
                    <FontAwesomeIcon icon={faBars} size="lg" /> Menu
                </NavbarToggler>
                <Link route="/">
                    <NavbarBrand
                        href="/"
                        className="d-xs-none d-sm-inline-block d-md-inline-block d-lg-inline-block d-xl-inline-block navbar-brand"
                    >
                        CTForces
                    </NavbarBrand>
                </Link>
                <NavbarToggler onClick={this.hideSidebar} className="border-0">
                    <FontAwesomeIcon icon={faBars} size="lg" />
                </NavbarToggler>
                <Collapse isOpen={this.state.isOpen} navbar>
                    <Nav navbar className="w-100 pull-left nav-fill mr-auto">
                        <NavItem>
                            <Link route="/" passHref>
                                <NavLink>Home</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link route="/" passHref>
                                <NavLink>Contests</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link route="/" passHref>
                                <NavLink>Tasks</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link route="/" passHref>
                                <NavLink>Upsolving</NavLink>
                            </Link>
                        </NavItem>
                        <NavItem>
                            <Link route="/" passHref>
                                <NavLink>Rating</NavLink>
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
                            <LoginButton authProp={this.props} />
                        </NavItem>
                        <NavItem className="mx-1 my-1">
                            <RegisterButton
                                authProp={this.props}
                                onClick={this.logout}
                            />
                        </NavItem>
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }
}

export default withAuth(MenuComponent);

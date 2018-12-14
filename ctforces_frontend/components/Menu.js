import React, { Component } from 'react';
import Router from 'next/router';
import Link from 'next/link';

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

class Menu extends Component {
    constructor(props) {
        super(props);
        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        };
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (
            <Navbar
                color="light"
                light
                sticky="top"
                expand="md"
                className="shadow-sm"
            >
                <Link href="/">
                    <NavbarBrand href="/">CTForces</NavbarBrand>
                </Link>
                <NavbarToggler onClick={this.toggle} />
                <Collapse isOpen={this.state.isOpen} navbar>
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
                            <Link href="login">
                                <Button color="primary" className="btn-block">
                                    Sign in
                                </Button>
                            </Link>
                        </NavItem>
                        <NavItem className="mx-1 my-1">
                            <Button className="btn-block">Sign out</Button>
                        </NavItem>
                    </Nav>
                </Collapse>
            </Navbar>
        );
    }
}

export default Menu;

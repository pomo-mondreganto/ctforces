import React, { Component } from 'react';
import Link from 'next/link';
import Logo from '../static/logo.png';
import Router from 'next/router';
import {
    Navbar,
    NavbarBrand,
    NavbarToggler,
    Collapse,
    Nav,
    NavItem,
    NavLink,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem
} from 'reactstrap';

class Menu extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isOpen: false
        };
    }

    loginRedirect = () => {
        Router.push('/login');
    };

    registerRedirect = () => {
        Router.push('/register');
    };

    toggle = () => {
        this.setState({
            isOpen: !this.state.isOpen
        });
    };

    render() {
        return (
            /*<div className="ui large nine item stackable menu">
                <Link href="/">
                    <a className="item">
                        <img src={Logo} alt="" />
                    </a>
                </Link>
                <Link href="/">
                    <a className="item">Home</a>
                </Link>
                <Link href="/">
                    <a className="item">Contests</a>
                </Link>
                <Link href="/">
                    <a className="item">Tasks</a>
                </Link>
                <Link href="/">
                    <a className="item">Upsolving</a>
                </Link>
                <Link href="/">
                    <a className="item">Rating</a>
                </Link>
                <div className="right item">
                    <button
                        className="ui primary button"
                        onClick={this.loginRedirect}
                    >
                        Sign In
                    </button>
                </div>
                <div className="item">
                    <button
                        className="ui button"
                        onClick={this.registerRedirect}
                    >
                        Sign Up
                    </button>
                </div>
            </div>*/
            <div>
                <Navbar color="light" light expand="md">
                    <div className="container">
                        <NavbarBrand href="/">
                            <img src={Logo} width={40} height={40} alt="" />
                        </NavbarBrand>
                        <NavbarToggler onClick={this.toggle} />
                        <Collapse isOpen={this.state.isOpen} navbar>
                            <Nav className="ml-auto" navbar>
                                <NavItem>
                                    <NavLink href="/components/">
                                        Components
                                    </NavLink>
                                </NavItem>
                                <NavItem>
                                    <NavLink href="https://github.com/reactstrap/reactstrap">
                                        GitHub
                                    </NavLink>
                                </NavItem>
                                <UncontrolledDropdown nav inNavbar>
                                    <DropdownToggle nav caret>
                                        Options
                                    </DropdownToggle>
                                    <DropdownMenu right>
                                        <DropdownItem>Option 1</DropdownItem>
                                        <DropdownItem>Option 2</DropdownItem>
                                        <DropdownItem divider />
                                        <DropdownItem>Reset</DropdownItem>
                                    </DropdownMenu>
                                </UncontrolledDropdown>
                            </Nav>
                        </Collapse>
                    </div>
                </Navbar>
            </div>
        );
    }
}

export default Menu;

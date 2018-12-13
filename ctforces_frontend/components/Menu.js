import React, {Component} from 'react';
import Router from 'next/router';


import {Button, Collapse, Nav, Navbar, NavbarBrand, NavbarToggler, NavItem, NavLink} from 'reactstrap';


class Menu extends Component {
  loginRedirect = () => {
    Router.push('/login');
  };
  registerRedirect = () => {
    Router.push('/register');
  };

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
      <Navbar color="light" light sticky="top" expand="md" className="shadow-sm">
        <NavbarBrand href="/">CTForces</NavbarBrand>
        <NavbarToggler onClick={this.toggle}/>
        <Collapse isOpen={this.state.isOpen} navbar>
          <Nav navbar className="w-100 nav-fill mr-auto">
            <NavItem>
              <NavLink active href="/">Home</NavLink>
            </NavItem>
            <NavItem>
              <NavLink active href="/">Contests</NavLink>
            </NavItem>
            <NavItem>
              <NavLink active href="/">Tasks</NavLink>
            </NavItem>
            <NavItem>
              <NavLink active href="/">Upsolving</NavLink>
            </NavItem>
            <NavItem>
              <NavLink active href="/">Rating</NavLink>
            </NavItem>
          </Nav>
        </Collapse>

        <Collapse isOpen={this.state.isOpen} navbar className="justify-content-end mr-auto ml-auto w-25">
          <Nav className="nav-fill" navbar>
            <NavItem className="mx-1 my-1">
              <Button color="danger" className="btn-block">
                Sign in
              </Button>
            </NavItem>
            <NavItem className="mx-1 my-1">
              <Button className="btn-block">
                Sign out
              </Button>
            </NavItem>
          </Nav>
        </Collapse>
      </Navbar>
    );
  }
}

export default Menu;

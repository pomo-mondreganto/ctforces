import React, { Component } from 'react';
import Link from 'next/link';
import Logo from '../static/logo.png';
import Router from 'next/router';

class Menu extends Component {
    constructor(props) {
        super(props);
    }

    loginRedirect = () => {
        Router.push('/login');
    };

    registerRedirect = () => {
        Router.push('/register');
    };

    render() {
        return (
            <div className="ui large nine item stackable menu">
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
            </div>
        );
    }
}

export default Menu;

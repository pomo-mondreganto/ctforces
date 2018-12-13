import 'bootstrap/dist/css/bootstrap.min.css';
import Menu from '../components/Menu';
import React, { Component } from 'react';
import Head from 'next/head';

class Layout extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Head>
                    <link
                        rel="stylesheet"
                        href="https://fonts.googleapis.com/css?family=Roboto:300,400,500"
                    />
                    <meta
                        name="viewport"
                        content="minimum-scale=1, initial-scale=1, width=device-width, shrink-to-fit=no"
                    />
                </Head>
                <Menu />
                <div className="container">{this.props.children}</div>
            </div>
        );
    }
}

export default Layout;

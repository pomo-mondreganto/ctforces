import 'bootstrap/dist/css/bootstrap.min.css';
import Menu from '../components/Menu';
import React, { Component } from 'react';

class Layout extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Menu />
                <div className="container">{this.props.children}</div>
            </div>
        );
    }
}

export default Layout;

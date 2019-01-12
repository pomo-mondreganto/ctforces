import 'bootstrap/dist/css/bootstrap.min.css';
import 'simplemde/dist/simplemde.min.css';
import MenuComponent from '../components/Menu';
import React, { Component } from 'react';

class Layout extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <MenuComponent />
                <div className="container my-4">{this.props.children}</div>
            </div>
        );
    }
}

export default Layout;

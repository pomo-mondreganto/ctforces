import 'semantic-ui-css/semantic.min.css';
import Menu from '../components/Menu';
import React, { Component } from 'react';

class Layout extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div className="ui container">
                <Menu />
                {this.props.children}
            </div>
        );
    }
}

export default Layout;

import Layout from '../layouts/master.js';
import React, {Component} from 'react';
import {login} from '../lib/AuthService';

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        };
    }

    handleSubmit = async event => {
        event.preventDefault();
        try {
            let data = await login(this.state.username, this.state.password);
        } catch (e) {}
    };

    handleChange = event => {
        let dispatch = {};
        dispatch[event.target.name] = event.target.value;
        this.setState(dispatch);
    };

    render() {
        return (
            <Layout>

            </Layout>
        );
    }
}

export default Login;

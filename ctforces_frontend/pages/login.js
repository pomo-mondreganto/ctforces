import Layout from '../layouts/master.js';
import withAuth from '../wrappers/withAuth';
import React, { Component } from 'react';
import { login } from '../lib/AuthService';

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
                <div className="ui segment">
                    <div>Sign In</div>
                    <div className="ui clearing divider" />
                    <form
                        onSubmit={this.handleSubmit}
                        className="ui basic vertical segment form error warning"
                    >
                        <div className="field">
                            <input
                                type="text"
                                name="username"
                                placeholder="Username"
                                value={this.username}
                                onChange={this.handleChange}
                            />
                        </div>
                        <div className="field">
                            <input
                                type="password"
                                name="password"
                                placeholder="Password"
                                value={this.password}
                                onChange={this.handleChange}
                            />
                        </div>
                        <button
                            className="ui fluid teal button field"
                            type="submit"
                        >
                            Sign me in
                        </button>
                    </form>
                </div>
            </Layout>
        );
    }
}

export default Login;

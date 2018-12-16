import Layout from '../layouts/master.js';
import React, { Component } from 'react';
import { login, getUser } from '../lib/auth_service';
import Link from 'next/link';
import withAuth from '../wrappers/withAuth';
import { AuthCtx } from '../wrappers/withAuth';
import validateFields, {
    required,
    validateOk,
    lengthGt,
    lengthBetween
} from '../lib/validators';

import {
    Button,
    Card,
    CardBody,
    CardHeader,
    CardLink,
    Col,
    Container,
    Form,
    FormGroup,
    Input,
    Label,
    Row,
    FormFeedback
} from 'reactstrap';

class Login extends Component {
    static contextType = AuthCtx;

    constructor(props) {
        super(props);
        this.state = {
            errors: {},
            formFields: {
                username: '',
                password: ''
            }
        };
    }

    validateChange = () => {
        let validateResult = validateFields(this.state.formFields, {
            username: [lengthBetween(5, 10)]
        });
        return validateResult;
    };

    validateSubmit = () => {
        let validateResult = validateFields(this.state.formFields, {
            username: [required]
        });
        return validateResult;
    };

    applyServerErrors = data => {
        let applyState = {};
        for (let key in data) {
            applyState[key] = [data[key]];
        }
        this.setState({
            errors: applyState
        });
    };

    handleSubmit = async event => {
        event.preventDefault();

        let validated = this.validateSubmit();
        this.setState({
            errors: validated.verdicts
        });

        if (validated.ok) {
            let data = await login(this.state.username, this.state.password);
            if (data.ok) {
                this.context.updateAuth(await getUser());
            } else {
                this.applyServerErrors(await data.json());
            }
        }
    };

    handleChange = event => {
        let dispatch = this.state.formFields;
        dispatch[event.target.name] = event.target.value;
        this.setState(dispatch);

        let validated = this.validateChange();
        this.setState({ errors: validated.verdicts });
    };

    render() {
        return (
            <Layout>
                <Row className="justify-content-center">
                    <Col className="col-xl-6 col-lg-6 col-md-8 col-sm-10 col-10 my-4">
                        <Card>
                            <CardHeader className="text-center">
                                Sign in
                            </CardHeader>
                            <CardBody>
                                <Form
                                    className="justify-content-center"
                                    onSubmit={this.handleSubmit}
                                >
                                    <FormGroup>
                                        <Input
                                            type="text"
                                            name="username"
                                            className="form-control"
                                            placeholder="username or email"
                                            autoFocus
                                            onChange={this.handleChange}
                                            invalid={
                                                'username' in this.state.errors
                                            }
                                        />
                                        {'username' in this.state.errors &&
                                            this.state.errors.username.map(
                                                (error, i) => (
                                                    <FormFeedback key={i}>
                                                        {error}
                                                    </FormFeedback>
                                                )
                                            )}
                                    </FormGroup>
                                    <FormGroup>
                                        <Input
                                            type="password"
                                            name="password"
                                            className="form-control"
                                            placeholder="password"
                                            onChange={this.handleChange}
                                            invalid={
                                                'password' in this.state.errors
                                            }
                                        />
                                        {'password' in this.state.errors &&
                                            this.state.errors.password.map(
                                                (error, i) => (
                                                    <FormFeedback key={i}>
                                                        {error}
                                                    </FormFeedback>
                                                )
                                            )}
                                    </FormGroup>
                                    <FormGroup>
                                        <Input
                                            hidden
                                            type="text"
                                            name="detail_error"
                                            className="form-control"
                                            placeholder="detail_error"
                                            invalid={
                                                'detail' in this.state.errors
                                            }
                                        />
                                        {'detail' in this.state.errors &&
                                            this.state.errors.detail.map(
                                                (error, i) => (
                                                    <FormFeedback key={i}>
                                                        {error}
                                                    </FormFeedback>
                                                )
                                            )}
                                    </FormGroup>
                                    <Button
                                        color="primary"
                                        className="btn-block"
                                        type="submit"
                                    >
                                        Submit
                                    </Button>
                                </Form>
                                <hr className="my-3" />
                                <Container>
                                    <Row>
                                        <Col className="text-left">
                                            <CardLink href="/restore_password">
                                                Forgot password
                                            </CardLink>
                                        </Col>
                                        <Col className="text-right">
                                            <Link href="register">
                                                <CardLink href="register">
                                                    Register
                                                </CardLink>
                                            </Link>
                                        </Col>
                                    </Row>
                                </Container>
                            </CardBody>
                        </Card>
                    </Col>
                </Row>
            </Layout>
        );
    }
}

export default Login;

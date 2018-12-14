import Layout from '../layouts/master.js';
import React, {Component} from 'react';
import {login} from '../lib/AuthService';
import Link from 'next/link';

import {Button, Card, CardBody, CardHeader, CardLink, Col, Container, Form, FormGroup, Input, Row} from 'reactstrap';

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
              <Row className="justify-content-center">
                <Col className="col-xl-6 col-lg-6 col-md-8 col-sm-10 col-10 my-4">
                  <Card>
                    <CardHeader className="text-center">
                      Sign in
                    </CardHeader>
                    <CardBody>
                      <Form className="justify-content-center">
                        <FormGroup>
                          <Input
                            type="text"
                            name="username"
                            className="form-control"
                            placeholder="username or email"
                            required
                            autoFocus
                          />
                        </FormGroup>
                        <FormGroup>
                          <Input
                            type="password"
                            name="password"
                            className="form-control"
                            placeholder="password"
                            required
                          />
                        </FormGroup>
                        <Button
                          color="primary"
                          className="btn-block"
                          type="submit"
                        >
                          Submit
                        </Button>
                      </Form>
                      <hr className="my-3"/>
                      <Container>
                        <Row>
                          <Col className="text-left">
                            <Link href="/restore_password">
                              <CardLink href="/restore_password">
                                Forgot password
                              </CardLink>
                            </Link>
                          </Col>
                          <Col className="text-right">
                            <Link href="/register">
                              <CardLink href="/register">
                                Sign in
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

import Layout from '../layouts/master.js';
import React, {Component} from 'react';
import {login} from '../lib/AuthService';

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
  Row
} from 'reactstrap';

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
                          <Label>Username or email</Label>
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
                          <Label>Password</Label>
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
                            <CardLink href="/restore_password">
                              Forgot password
                            </CardLink>
                          </Col>
                          <Col className="text-right">
                            <CardLink href="/register">
                              Register
                            </CardLink>
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

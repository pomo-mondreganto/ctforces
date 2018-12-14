import Layout from '../layouts/master.js';
import React, {Component} from 'react';
import Link from 'next/link';

import {
  Button,
  Card,
  CardBody,
  CardHeader,
  CardLink,
  Col,
  Container,
  Form,
  FormFeedback,
  FormGroup,
  Input,
  Row
} from 'reactstrap';

class Register extends Component {
  handleSubmit = async event => {
    // write this shit
  };
  handleChange = event => {
    let dispatch = {};
    dispatch[event.target.name] = event.target.value;

    if (
      event.target.name == 'confirm_password' ||
      event.target.name == 'password'
    ) {
      if (event.target.name == 'confirm_password') {
        dispatch['password'] = this.state['password'];
      }
      if (
        !dispatch['confirm_password'] ||
        dispatch['password'] === dispatch['confirm_password']
      ) {
        this.setState({
          passwords_match: true
        });
      } else if (dispatch['password'] !== dispatch['confirm_password']) {
        this.setState({
          passwords_match: false
        });
      }
    }

    this.setState(dispatch);
  };

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      email: '',
      password: '',
      confirm_password: '',
      passwords_match: true
    };
  }

  render() {
    return (
      <Layout>
        <Row className="justify-content-center">
          <Col className="col-xl-6 col-lg-6 col-md-8 col-sm-10 col-10 my-4">
            <Card>
              <CardHeader className="text-center">
                Register
              </CardHeader>
              <CardBody>
                <Form className="justify-content-center">
                  <FormGroup>
                    <Input
                      type="text"
                      name="username"
                      className="form-control"
                      placeholder="username"
                      required
                      autoFocus
                      onChange={this.handleChange}
                    />
                  </FormGroup>
                  <FormGroup>
                    <Input
                      type="text"
                      name="email"
                      className="form-control"
                      placeholder="email"
                      required
                      onChange={this.handleChange}
                    />
                  </FormGroup>
                  <FormGroup>
                    <Input
                      type="password"
                      name="password"
                      className="form-control"
                      placeholder="password"
                      required
                      onChange={this.handleChange}
                    />
                  </FormGroup>
                  <FormGroup>
                    <Input
                      type="password"
                      name="confirm_password"
                      className="form-control"
                      placeholder="confirm password"
                      required
                      invalid={
                        !this.state.passwords_match
                      }
                      valid={
                        this.state.passwords_match &&
                        this.state.confirm_password !==
                        ''
                      }
                      onChange={this.handleChange}
                    />
                    <FormFeedback>
                      Passwords do not match
                    </FormFeedback>
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
                      <Link href="/login">
                        <CardLink href="/login">
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

export default Register;

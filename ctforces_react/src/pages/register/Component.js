import React from 'react';

import { LinkContainerNonActive } from '../../lib/LinkContainer';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import TextInput from '../../components/Form/TextInput/Container';
import DetailError from '../../components/Form/DetailError/Container';
import Layout from '../../layouts/sidebar/Container';
import withLayout from '../../wrappers/withLayout';

import {
    Card,
    CardBody,
    CardHeader,
    CardLink,
    Col,
    Row,
    Button
} from 'reactstrap';

const Component = props => {
    return (
        <Row className="justify-content-center">
            <Col className="col-xl-6 col-lg-6 col-md-8 col-sm-10 col-10 my-4">
                <Card>
                    <CardHeader className="text-center">Sign in</CardHeader>
                    <CardBody>
                        <Formik
                            initialValues={{
                                username: '',
                                password: '',
                                email: ''
                            }}
                            onSubmit={(values, actions) => {
                                props.handleSubmit({ values, actions });
                            }}
                        >
                            {({ isSubmitting, errors }) => (
                                <Form>
                                    <Field
                                        type="text"
                                        name="username"
                                        placeholder="Username"
                                        component={TextInput}
                                    />
                                    <Field
                                        type="email"
                                        name="email"
                                        placeholder="Email"
                                        component={TextInput}
                                    />
                                    <Field
                                        type="password"
                                        name="password"
                                        placeholder="Password"
                                        component={TextInput}
                                    />
                                    <Field component={DetailError} />
                                    <Button
                                        type="submit"
                                        color="primary"
                                        className="btn-block"
                                        disabled={isSubmitting}
                                    >
                                        Register
                                    </Button>
                                </Form>
                            )}
                        </Formik>
                        <hr className="my-3" />
                        <Row>
                            <Col className="text-left">
                                <LinkContainerNonActive to="/restore_password">
                                    <CardLink>Forgot password</CardLink>
                                </LinkContainerNonActive>
                            </Col>
                            <Col className="text-right">
                                <LinkContainerNonActive to="/login">
                                    <CardLink>Log In</CardLink>
                                </LinkContainerNonActive>
                            </Col>
                        </Row>
                    </CardBody>
                </Card>
            </Col>
        </Row>
    );
};

export default withLayout(Component, Layout);

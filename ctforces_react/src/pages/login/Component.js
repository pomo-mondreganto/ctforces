import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    Card, CardBody, CardHeader, CardLink, Button,
} from 'reactstrap';
import { LinkContainerNonActive } from '../../lib/LinkContainer';
import TextInput from '../../components/Form/TextInput/Container';
import DetailError from '../../components/Form/DetailError/Container';
import Layout from '../../layouts/sidebar/Container';
import withLayout from '../../wrappers/withLayout';


const Component = props => (
    <section>
        <article>
            <Card>
                <CardHeader className="text-center">Sign in</CardHeader>
                <CardBody>
                    <Formik
                        initialValues={{
                            username: '',
                            password: '',
                        }}
                        onSubmit={(values, actions) => {
                            props.handleSubmit({ values, actions });
                        }}
                    >
                        {({ isSubmitting }) => (
                            <Form>
                                <Field
                                    type="text"
                                    name="username"
                                    placeholder="Username"
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
                                    Log In
                                </Button>
                            </Form>
                        )}
                    </Formik>

                    <hr className="my-3" />
                    <div>
                        <span className="float-left">
                            <LinkContainerNonActive to="/restore_password">
                                <CardLink>Forgot password</CardLink>
                            </LinkContainerNonActive>
                        </span>
                        <span className="float-right">
                            <LinkContainerNonActive to="/register">
                                <CardLink>Register</CardLink>
                            </LinkContainerNonActive>
                        </span>
                    </div>
                </CardBody>
            </Card>
        </article>
    </section>
);

export default withLayout(Component, Layout);

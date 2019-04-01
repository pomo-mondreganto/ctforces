import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    Button,
} from 'reactstrap';
import { LinkContainerNonActive } from 'lib/LinkContainer';
import TextInput from 'components/Form/TextInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabs from 'components/CardWithTabs/Container';

const Component = props => (
    <section>
        <article>
            <CardWithTabs
                title="Login"
            >
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
                                Login
                            </Button>
                        </Form>
                    )}
                </Formik>

                <hr className="my-3" />
                <div className="mb-5 mt-4">
                    <span className="float-left">
                        <LinkContainerNonActive to="/restore_password/">
                            <a>Forgot password</a>
                        </LinkContainerNonActive>
                    </span>
                    <span className="float-right">
                        <LinkContainerNonActive to="/register/">
                            <a>Register</a>
                        </LinkContainerNonActive>
                    </span>
                </div>
            </CardWithTabs>
        </article>
    </section>
);

export default withLayout(Component, Layout);

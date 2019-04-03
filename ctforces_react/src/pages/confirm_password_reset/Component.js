import React from 'react';

import { Formik, Form, Field } from 'formik';
import {
    Button,
} from 'reactstrap';
import TextInput from 'components/Form/TextInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';

import CardWithTabs from 'components/CardWithTabs/Container';

const Component = props => (
    <section>
        <article>
            <CardWithTabs
                title="Reset password"
            >
                <Formik
                    enableReinitialize
                    initialValues={{
                        password: '',
                        token: props.token,
                    }}
                    onSubmit={(values, actions) => {
                        props.handleSubmit({ values, actions });
                    }}
                >
                    {({ isSubmitting }) => (
                        <Form>
                            <Field
                                type="password"
                                name="password"
                                placeholder="Password"
                                component={TextInput}
                            />
                            <Field
                                type="text"
                                name="token"
                                hidden
                                component={TextInput}
                            />
                            <Field component={DetailError} />
                            <Button
                                type="submit"
                                color="primary"
                                className="btn-block"
                                disabled={isSubmitting}
                            >
                                Reset password
                            </Button>
                        </Form>
                    )}
                </Formik>
            </CardWithTabs>
        </article>
    </section>
);

export default withLayout(Component, Layout);

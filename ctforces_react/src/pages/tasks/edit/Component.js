import React from 'react';

import { Card, Button } from 'reactstrap';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';
import { Formik, Form, Field } from 'formik';
import TextInput from '../../../components/Form/TextInput/Container';
import CheckboxInput from '../../../components/Form/CheckboxInput/Container';
import SimpleMDEInput from '../../../components/Form/SimpleMDEInput/Container';
import DetailError from '../../../components/Form/DetailError/Container';
import TagsInput from '../../../components/Form/TagsInput/Container';
import FilesInput from '../../../components/Form/FilesInput/Container';

const Component = props => {
    const {
        name = '',
        task_tags_details = [],
        cost = '',
        flag = '',
        description = '',
        files_details = [],
        is_published = false
    } = { ...props.task };

    const tags = task_tags_details.map((obj, i) => {
        return obj.name;
    });

    const files = files_details.map((obj, i) => {
        return {
            name: obj.name,
            uploaded: true,
            id: obj.id
        };
    });

    return (
        <Card className="p-2">
            <div style={{ fontSize: '2rem' }} className="py-2">
                Edit task
            </div>
            <hr />
            <Formik
                enableReinitialize
                initialValues={{
                    name,
                    tags,
                    cost,
                    flag,
                    description,
                    files,
                    is_published
                }}
                onSubmit={(values, actions) => {
                    props.handleSubmit({ values, actions });
                }}
            >
                {({ isSubmitting }) => (
                    <Form>
                        <Field
                            type="text"
                            name="name"
                            placeholder="Name"
                            component={TextInput}
                        />
                        <Field name="tags" component={TagsInput} />
                        <Field
                            type="text"
                            name="cost"
                            placeholder="Cost"
                            component={TextInput}
                        />
                        <Field
                            type="text"
                            name="flag"
                            placeholder="Flag"
                            component={TextInput}
                        />
                        <Field name="description" component={SimpleMDEInput} />
                        <Field
                            type="checkbox"
                            name="is_published"
                            label="publish"
                            component={CheckboxInput}
                        />
                        <Field name="files" component={FilesInput} multiple />
                        <Field component={DetailError} />
                        <Button
                            type="submit"
                            color="primary"
                            className="btn-block"
                            disabled={isSubmitting}
                        >
                            Edit
                        </Button>
                    </Form>
                )}
            </Formik>
        </Card>
    );
};

export default withLayout(Component, Layout);

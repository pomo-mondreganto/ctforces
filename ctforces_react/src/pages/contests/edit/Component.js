import React from 'react';

import { Card, Button } from 'reactstrap';
import Layout from '../../../layouts/sidebar/Container';
import withLayout from '../../../wrappers/withLayout';
import { Formik, Form, Field, FieldArray } from 'formik';
import TextInput from '../../../components/Form/TextInput/Container';
import CheckboxInput from '../../../components/Form/CheckboxInput/Container';
import SimpleMDEInput from '../../../components/Form/SimpleMDEInput/Container';
import DetailError from '../../../components/Form/DetailError/Container';
import TagsInput from '../../../components/Form/TagsInput/Container';
import CalendarInput from '../../../components/Form/CalendarInput/Container';
import DatetimeInput from 'react-datetime';
import moment from 'moment';
import TaskPreviewInput from '../components/TaskPreview/Container';

const Component = props => {
    const {
        name = '',
        description = '',
        contest_task_relationship_details = [],
        is_published = false,
        is_registration_open = false,
        is_rated = false,
        is_running = false,
        publish_tasks_after_finished = false,
        is_finished = false,
        start_time = moment().toISOString(),
        end_time = moment().toISOString()
    } = { ...props.contest };

    console.log(props.contest);

    const tasks = [{ id: '', name: '', cost: '', main_tag: '' }];

    return (
        <Card className="p-2">
            <div style={{ fontSize: '2rem' }} className="py-2">
                Edit contest
            </div>
            <hr />
            <Formik
                enableReinitialize
                initialValues={{
                    name,
                    description,
                    tasks,
                    is_published,
                    is_registration_open,
                    is_rated,
                    is_running,
                    publish_tasks_after_finished,
                    is_finished,
                    start_time,
                    end_time
                }}
                onSubmit={(values, actions) => {
                    props.handleSubmit({ values, actions });
                }}
            >
                {({ isSubmitting, values }) => (
                    <Form>
                        <Field
                            type="text"
                            name="name"
                            placeholder="Name"
                            component={TextInput}
                        />

                        <Field
                            type="text"
                            name="description"
                            placeholder="Description"
                            component={TextInput}
                        />

                        <FieldArray
                            name="tasks"
                            render={arrayHelpers => (
                                <>
                                    {values.tasks.map((obj, i) => {
                                        return (
                                            <div key={i}>
                                                <Field
                                                    name={`tasks.${i}`}
                                                    component={TaskPreviewInput}
                                                />

                                                <button
                                                    type="button"
                                                    onClick={() =>
                                                        arrayHelpers.remove(i)
                                                    }
                                                >
                                                    remove
                                                </button>
                                            </div>
                                        );
                                    })}
                                    <button
                                        type="button"
                                        onClick={() =>
                                            arrayHelpers.push({
                                                id: '',
                                                name: ''
                                            })
                                        }
                                    >
                                        add task
                                    </button>
                                </>
                            )}
                        />

                        <Field
                            type="checkbox"
                            name="is_published"
                            label="Published"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_registration_open"
                            label="Registration is opened"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_rated"
                            label="Rated"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_running"
                            label="Running"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="publish_tasks_after_finished"
                            label="Publish tasks after contest is finished"
                            component={CheckboxInput}
                        />

                        <Field
                            type="checkbox"
                            name="is_finished"
                            label="Finished"
                            component={CheckboxInput}
                        />

                        <label>Start time</label>
                        <Field name="start_time" component={CalendarInput} />

                        <label>End time</label>
                        <Field name="end_time" component={CalendarInput} />

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

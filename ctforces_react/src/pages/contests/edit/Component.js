import React from 'react';

import { Button } from 'reactstrap';
import {
    Formik, Form, Field, FieldArray,
} from 'formik';
import moment from 'moment';
import Layout from 'layouts/sidebar/Container';
import withLayout from 'wrappers/withLayout';
import TextInput from 'components/Form/TextInput/Container';
import CheckboxInput from 'components/Form/CheckboxInput/Container';
import DetailError from 'components/Form/DetailError/Container';
import CalendarInput from 'components/Form/CalendarInput/Container';
import CardWithTabs from 'components/CardWithTabs/Container';
import TaskPreviewInput from '../components/TaskPreview/Container';

const Component = (props) => {
    const {
        name = '',
        description = '',
        is_published: isPublished = false,
        is_registration_open: isRegistrationOpen = false,
        is_rated: isRated = false,
        is_running: isRunning = false,
        publish_tasks_after_finished: publishTasksAfterFinished = false,
        is_finished: isFinished = false,
    } = { ...props.contest };

    let {

        start_time: startTime = '',
        end_time: endTime = '',
    } = { ...props.contest };

    const {
        contest_task_relationship_details: tasksRelationships = [],
    } = { ...props.contest };

    startTime = moment(startTime);
    endTime = moment(endTime);

    const tasks = tasksRelationships.map(relationship => ({
        id: relationship.task,
        name: relationship.task_name,
        cost: relationship.cost,
        main_tag: relationship.main_tag_details,
    }));

    return (
        <CardWithTabs
            title="Edit contest"
        >
            <hr />
            <Formik
                enableReinitialize
                initialValues={{
                    name,
                    description,
                    tasks,
                    is_published: isPublished,
                    is_registration_open: isRegistrationOpen,
                    is_rated: isRated,
                    is_running: isRunning,
                    publish_tasks_after_finished: publishTasksAfterFinished,
                    is_finished: isFinished,
                    start_time: startTime,
                    end_time: endTime,
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
                                    {values.tasks.map((obj, i) => (
                                        <div key={i} className="task-add-preview mb-4">
                                            <Field
                                                name={`tasks[${i}]`}
                                                component={TaskPreviewInput}
                                            />
                                            <div className="task-add-buttons">
                                                <Button
                                                    type="button"
                                                    onClick={() => arrayHelpers.insert(i + 1, {
                                                        id: '', name: '', cost: '', main_tag: {},
                                                    })}
                                                    className="task-add-button-add"
                                                    outline
                                                    color="success"
                                                    size="sm"
                                                >
                                                    Add task
                                                </Button>
                                                <Button
                                                    type="button"
                                                    onClick={() => {
                                                        arrayHelpers.remove(i);
                                                    }}
                                                    className="task-add-button-remove"
                                                    outline
                                                    color="danger"
                                                    size="sm"
                                                >
                                                    Remove
                                                </Button>
                                            </div>
                                        </div>
                                    ))}
                                    {values.tasks.length === 0 && (
                                        <div className="task-add-buttons mb-4">
                                            <Button
                                                type="button"
                                                onClick={() => arrayHelpers.insert(0, {
                                                    id: '', name: '', cost: '', main_tag: {},
                                                })}
                                                className="task-add-button-add"
                                                outline
                                                color="success"
                                                size="sm"
                                            >
                                                Add task
                                            </Button>
                                            <Button
                                                type="button"
                                                onClick={() => {
                                                    arrayHelpers.remove(0);
                                                }}
                                                disabled
                                                className="task-add-button-remove"
                                                outline
                                                color="danger"
                                                size="sm"
                                            >
                                                Remove
                                            </Button>
                                        </div>
                                    )}
                                </>
                            )}
                        />

                        <Field
                            name="is_published"
                            label="Published"
                            component={CheckboxInput}
                        />

                        <Field
                            name="is_registration_open"
                            label="Registration is opened"
                            component={CheckboxInput}
                        />

                        <Field
                            name="is_rated"
                            label="Rated"
                            component={CheckboxInput}
                        />

                        <Field
                            name="is_running"
                            label="Running"
                            component={CheckboxInput}
                        />

                        <Field
                            name="publish_tasks_after_finished"
                            label="Publish tasks after contest is finished"
                            component={CheckboxInput}
                        />

                        <Field
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
        </CardWithTabs>
    );
};

export default withLayout(Component, Layout);

import React, { Component } from 'react';
import { Form, FormGroup, Input, Button, FormFeedback } from 'reactstrap';
import validate from '../lib/validators';
import TextInputComponent from './TextInput';

class InputComponent extends Component {
    constructor(props) {
        super(props);
        let initial_value = '';
        if (this.props.initial_value !== undefined) {
            initial_value = this.props.initial_value;
        }
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: initial_value
            }
        });
    }

    render() {
        if (this.props.source !== undefined) {
            const CustomInput = this.props.source;
            return (
                <FormGroup>
                    <CustomInput
                        name={this.props.name}
                        handleChange={this.props.handleChange}
                        initial_value={this.props.initial_value}
                        {...this.props.pass_props}
                    />
                    <Input
                        invalid={this.props.name in this.props.errors}
                        hidden
                    />
                    {this.props.name in this.props.errors &&
                        this.props.errors[this.props.name].map((error, i) => (
                            <FormFeedback key={i}>{error}</FormFeedback>
                        ))}
                </FormGroup>
            );
        }
        return (
            <FormGroup>
                <TextInputComponent
                    initial_value={this.props.initial_value}
                    type={this.props.type}
                    name={this.props.name}
                    hidden={this.props.hidden}
                    placeholder={this.props.placeholder}
                    handleChange={this.props.handleChange}
                    invalid={this.props.name in this.props.errors}
                    errors={this.props.errors}
                />

                {this.props.name in this.props.errors &&
                    this.props.errors[this.props.name].map((error, i) => (
                        <FormFeedback key={i}>{error}</FormFeedback>
                    ))}
            </FormGroup>
        );
    }
}

class FormComponent extends Component {
    constructor(props) {
        super(props);

        let formFieldsValues = {};
        let formFields = [];

        for (let key in this.props.fields) {
            let field = this.props.fields[key];
            formFieldsValues[field.name] = '';
            formFields.push(field);
        }

        formFields.push({ name: 'detail', hidden: true });

        this.state = {
            errors: {},
            formFieldsValues: formFieldsValues,
            formFields: formFields
        };
    }

    validate = validate_empty => {
        let validateResultAll = {};
        let ok = true;
        for (let key in this.state.formFields) {
            let field = this.state.formFields[key];
            if (
                !validate_empty &&
                this.state.formFieldsValues[field.name] === ''
            ) {
                continue;
            }
            let validateResult = validate(
                this.state.formFieldsValues[field.name],
                field.validators === undefined ? [] : field.validators,
                this.state.formFieldsValues
            );
            if (validateResult) {
                validateResultAll[field.name] = validateResult;
                ok = false;
            }
        }
        return {
            ok: ok,
            verdicts: validateResultAll
        };
    };

    applyServerErrors = data => {
        let applyState = {};
        for (let key in data) {
            applyState[key] = [data[key]];
        }
        this.setState({
            errors: applyState
        });
    };

    handleSubmit = async event => {
        event.preventDefault();

        let validated = this.validate(true);
        this.setState({
            errors: validated.verdicts
        });
        if (validated.ok) {
            let result = await this.props.onOkSubmit(
                this.state.formFieldsValues
            );
            if (!result.ok) {
                this.applyServerErrors(result.errors);
            }
        }
    };

    handleChange = event => {
        let dispatch = this.state.formFieldsValues;
        dispatch[event.target.name] = event.target.value;
        this.setState(dispatch);

        let validated = this.validate(false);
        this.setState({ errors: validated.verdicts });
    };

    render() {
        return (
            <Form
                className="justify-content-center"
                onSubmit={this.handleSubmit}
            >
                {this.state.formFields.map((obj, i) => {
                    return (
                        <InputComponent
                            initial_value={obj.initial_value}
                            pass_props={obj.pass_props}
                            source={obj.source}
                            type={obj.type}
                            name={obj.name}
                            hidden={obj.hidden}
                            placeholder={obj.placeholder}
                            handleChange={this.handleChange}
                            errors={this.state.errors}
                            key={i}
                        />
                    );
                })}
                <Button color="primary" className="btn-block" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }
}

export default FormComponent;

import React, { Component } from 'react';
import { Button, Form, FormFeedback, FormGroup, Input } from 'reactstrap';
import validate from '../lib/validators';
import CheckBoxComponent from './CheckBoxInput';
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
        this.InputRef = React.createRef();
    }

    beforeSubmit = () => {
        if (this.InputRef.current.beforeSubmit !== undefined) {
            this.InputRef.current.beforeSubmit();
        }
    };

    render() {
        const CustomInputComponent = this.props.source;
        return (
            <FormGroup check={CustomInputComponent === CheckBoxComponent}>
                <CustomInputComponent
                    name={this.props.name}
                    handleChange={this.props.handleChange}
                    initial_value={this.props.initial_value}
                    hidden={this.props.hidden}
                    type={this.props.type}
                    {...this.props.pass_props}
                    invalid={this.props.name in this.props.errors}
                    placeholder={this.props.placeholder}
                    ref={this.InputRef}
                />
                <Input hidden invalid={this.props.name in this.props.errors} />
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
            field['react_ref'] = React.createRef();
            formFields.push(field);
        }

        formFields.push({
            name: 'detail',
            hidden: true,
            source: TextInputComponent
        });

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
            for (let key in this.props.fields) {
                this.state.formFields[key].react_ref.current.beforeSubmit();
            }
            if (this.props.onOkSubmit !== undefined) {
                let result = await this.props.onOkSubmit(
                    this.state.formFieldsValues
                );
                if (!result.ok) {
                    this.applyServerErrors(result.errors);
                }
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
                            ref={obj.react_ref}
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

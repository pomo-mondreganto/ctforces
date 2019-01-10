import React, {Component} from 'react';

import {Input} from 'reactstrap';

class TextInputComponent extends Component {
    constructor(props) {
        super(props);
        let initial_value = '';
        if (this.props.initial_value !== undefined) {
            initial_value = this.props.initial_value;
        }
        this.state = {value: initial_value};
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: initial_value
            }
        });
    }

    handleChange = event => {
        this.setState({
            value: event.target.value
        });
        this.props.handleChange(event);
    };

    render() {
        return (
            <Input
                type={this.props.type === undefined ? 'text' : this.props.type}
                name={
                    this.props.name === undefined ? 'default' : this.props.name
                }
                hidden={
                    this.props.hidden === undefined ? false : this.props.hidden
                }
                value={this.state.value}
                className="form-control"
                placeholder={this.props.placeholder}
                onChange={this.handleChange}
                invalid={this.props.invalid}
            />
        );
    }
}

export default TextInputComponent;

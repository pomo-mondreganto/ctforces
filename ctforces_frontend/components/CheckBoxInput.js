import React, {Component} from 'react';

import {FormGroup, Input, Label} from 'reactstrap';

class CheckBoxComponent extends Component {
    constructor(props) {
        super(props);
        let initial_value = false;
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

    handleChange = () => {
        let current_value = this.state.value;
        this.setState({
            value: !current_value
        });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: !current_value
            }
        });
    };

    render() {
        return (
            <FormGroup check>
                <Label check>
                    <Input
                        type="checkbox"
                        name={this.props.name}
                        onChange={this.handleChange}
                        checked={this.state.value}
                    />{' '}
                    Publish
                </Label>
            </FormGroup>
        );
    }
}

export default CheckBoxComponent;

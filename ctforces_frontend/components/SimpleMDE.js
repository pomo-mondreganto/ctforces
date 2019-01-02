import SimpleMDE from 'react-simplemde-editor';
import React, { Component } from 'react';

class SimpleMDEComponent extends Component {
    constructor(props) {
        super(props);
        this.state = { textarea_value: '' };
    }

    handleMDEChange = value => {
        this.setState({
            textarea_value: value
        });
        this.props.handleChange({
            target: {
                name: this.props.name,
                value: value
            }
        });
    };

    render() {
        return (
            <SimpleMDE
                id={this.props.id}
                onChange={this.handleMDEChange}
                value={this.state.textarea_value}
                options={{
                    spellChecker: false
                }}
            />
        );
    }
}

export default SimpleMDEComponent;

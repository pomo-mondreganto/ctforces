import React from 'react';

import Component from './Component';

class SimpleMDEContainer extends React.Component {
    handleChange = (value) => {
        const { name } = this.props.field;
        this.props.form.setFieldValue(name, value);
    };

    render() {
        return <Component handleChange={this.handleChange} {...this.props} />;
    }
}

export default SimpleMDEContainer;

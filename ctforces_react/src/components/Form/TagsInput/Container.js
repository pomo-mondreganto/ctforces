import React from 'react';

import Component from './Component';

class TagsContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    handleChange = tags => {
        const { name } = this.props.field;
        this.props.form.setFieldValue(name, tags);
    };

    render() {
        return <Component handleChange={this.handleChange} {...this.props} />;
    }
}

export default TagsContainer;

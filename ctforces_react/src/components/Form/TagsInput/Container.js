import React from 'react';

import Component from './Component';

class TagsContainer extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            tags: []
        };
    }

    handleChange = tags => {
        const { name } = this.props.field;
        this.props.form.setFieldValue(name, tags);
        this.setState({ tags });
    };

    render() {
        return (
            <Component
                tags={this.state.tags}
                handleChange={this.handleChange}
                {...this.props}
            />
        );
    }
}

export default TagsContainer;

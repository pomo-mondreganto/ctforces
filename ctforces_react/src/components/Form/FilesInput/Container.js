import React from 'react';

import Component from './Component';

class FilesContainer extends React.Component {
    constructor(props) {
        super(props);
    }

    handleSelectedFiles = e => {
        const { files } = e.target;
        const { name } = this.props.field;
        const old_files = this.props.field.value;
        this.props.form.setFieldValue(
            name,
            Array.from(old_files).concat(Array.from(files))
        );
    };

    handleRemove = index => {
        const { name } = this.props.field;
        const files = this.props.field.value;
        files.splice(index, 1);
        this.props.form.setFieldValue(name, files);
    };

    render() {
        return (
            <Component
                {...this.props}
                handleSelectedFiles={this.handleSelectedFiles}
                handleRemove={this.handleRemove}
            />
        );
    }
}

export default FilesContainer;

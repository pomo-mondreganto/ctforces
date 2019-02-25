import React from 'react';

import Component from './Component';

class FilesContainer extends React.Component {
    constructor(props) {
        super(props);

        this.inputRef = React.createRef();
    }

    handleSelectedFiles = (e) => {
        const { files } = e.target;
        const { name } = this.props.field;
        const oldFiles = this.props.field.value;
        this.props.form.setFieldValue(
            name,
            Array.from(oldFiles).concat(Array.from(files)),
        );
        this.inputRef.value = '';
    };

    handleRemove = (index) => {
        const { name } = this.props.field;
        const files = this.props.field.value;
        files.splice(index, 1);
        this.props.form.setFieldValue(name, files);
    };

    render() {
        return (
            <Component
                ref={(input) => {
                    this.inputRef = input;
                }}
                {...this.props}
                handleSelectedFiles={this.handleSelectedFiles}
                handleRemove={this.handleRemove}
            />
        );
    }
}

export default FilesContainer;

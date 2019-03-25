import React from 'react';

import {
    FormGroup,
    FormFeedback,
    CustomInput,
    Progress,
    Button,
} from 'reactstrap';

const Component = React.forwardRef(
    ({
        field, form, multiple = false, ...props
    }, ref) => {
        const { name } = field;
        const invalid = form.errors[name] && form.errors[name] && true;
        const { uploading = {} } = { ...form.status };
        return (
            <FormGroup>
                <CustomInput
                    className="pb-5"
                    type="file"
                    id={`file-input-${field.name}`}
                    name={field.name}
                    onChange={props.handleSelectedFiles}
                    invalid={invalid}
                    multiple={multiple}
                    innerRef={ref}
                />
                {field.value.map((obj, index) => (
                    <div key={index} className="my-3">
                        <Button
                            className="mr-3"
                            onClick={() => {
                                props.handleRemove(index);
                            }}
                        >
                            Remove{' '}
                        </Button>
                        <span>{obj.name}</span>
                        <Progress
                            className="mt-3"
                            hidden={uploading[obj.name] === undefined}
                            value={uploading[obj.name] || 0}
                        />
                    </div>
                ))}
                <FormFeedback>{form.errors[name]}</FormFeedback>
            </FormGroup>
        );
    },
);

Component.displayName = 'FilesInputComponent';

export default Component;

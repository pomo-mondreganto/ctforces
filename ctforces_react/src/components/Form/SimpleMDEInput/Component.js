import React from 'react';

import SimpleMDE from 'react-simplemde-editor';
import { FormGroup, FormFeedback } from 'reactstrap';
import ReactMarkdown from 'react-markdown';
import ReactDOMServer from 'react-dom/server';

import 'node_modules/easymde/dist/easymde.min.css';

const Component = ({ field, form, handleChange }) => (
    <FormGroup>
        <SimpleMDE
            onChange={handleChange}
            value={field.value}
            options={{
                autofocus: true,
                spellChecker: false,
                previewRender(text) {
                    return ReactDOMServer.renderToString(
                        <ReactMarkdown
                            source={text}
                        />,
                    );
                },
            }}
        />
        <FormFeedback>{form.errors[field.name]}</FormFeedback>
    </FormGroup>
);

export default Component;

import React from 'react';
import ReactMarkdown from 'react-markdown';

const Component = props => <ReactMarkdown
    source={props.text}
/>;

export default Component;

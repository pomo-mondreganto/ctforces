/* eslint-disable no-shadow */
/* eslint-disable react/display-name */
import React from 'react';
import ReactMarkdown from 'react-markdown';

import RemarkMathPlugin from 'remark-math';
import 'node_modules/katex/dist/katex.min.css';
import TeX from '@matejmazur/react-katex';

const Component = (props) => {
    const newProps = {
        ...props,
        plugins: [
            RemarkMathPlugin,
        ],
        renderers: {
            ...props.renderers,
            math: props => <TeX math={props.value} block />,
            inlineMath: props => <TeX math={props.value} />,
        },
    };
    return (
        <ReactMarkdown {...newProps} source={newProps.text} />
    );
};

export default Component;

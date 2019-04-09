/* eslint-disable react/display-name */
import React from 'react';
import ReactMarkdown from 'react-markdown';

import RemarkMathPlugin from 'remark-math';
import 'node_modules/katex/dist/katex.min.css';
import TeX from '@matejmazur/react-katex';

import 'styles/components/Markdown.scss';

const Component = (props) => {
    const newProps = {
        ...props,
        plugins: [
            RemarkMathPlugin,
        ],
        renderers: {
            ...props.renderers,
            math: texBlockProps => <TeX math={texBlockProps.value} block />,
            inlineMath: texInlineProps => <TeX math={texInlineProps.value} />,
        },
    };
    return (
        <ReactMarkdown {...newProps} source={newProps.text} className="markdown" />
    );
};

export default Component;

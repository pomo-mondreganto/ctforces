import React from 'react';
import ReactMarkdown from 'react-markdown';
import RemarkMathPlugin from 'remark-math';
import { InlineMath, BlockMath } from 'react-katex';

const MarkdownRender = props => {
    const newProps = {
        ...props,
        plugins: [RemarkMathPlugin],
        renderers: {
            ...props.renderers,
            math: ({ value }) => <BlockMath>{value}</BlockMath>,
            inlineMath: ({ value }) => <InlineMath>{value}</InlineMath>
        }
    };
    return <ReactMarkdown {...newProps} />;
};

export default MarkdownRender;

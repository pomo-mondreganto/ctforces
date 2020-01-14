<template>
    <div class="markdown-body wb-a" ref="markdown-body"></div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import Katex from 'katex';
import MarkdownItTexmath from 'markdown-it-texmath';
import MarkdownItPrism from 'markdown-it-prism';

import 'prismjs/themes/prism.css';

import 'prismjs/components/prism-bash';
import 'prismjs/components/prism-csharp';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-json';
import 'prismjs/components/prism-nginx';
import 'prismjs/components/prism-perl';
import 'prismjs/components/prism-ruby';
import 'prismjs/components/prism-typescript';
import 'prismjs/components/prism-yaml';
import 'prismjs/components/prism-python';
import 'prismjs/components/prism-java';
import 'prismjs/components/prism-c';
import 'prismjs/components/prism-cpp';

export default {
    props: {
        content: {
            type: String,
            required: true,
        },
    },
    watch: {
        content: {
            immediate: true,
            handler(val) {
                this.$nextTick(() => {
                    this.$refs['markdown-body'].innerHTML = this.md.render(val);
                });
            },
        },
    },
    data: function() {
        let md = MarkdownIt({
            linkify: true,
        });

        let tm = MarkdownItTexmath;

        tm.use(Katex);

        md.use(tm, {
            delimiters: 'dollars',
        });

        md.use(MarkdownItPrism, {
            defaultLanguage: 'python',
        });

        return {
            md,
        };
    },
};
</script>

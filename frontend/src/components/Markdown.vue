<template>
    <div class="markdown-body" ref="markdown-body"></div>
</template>

<script>
import md from '@/utils/markdown';

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
                    this.$refs['markdown-body'].innerHTML = md.render(val);
                });
            },
        },
    },
};
</script>

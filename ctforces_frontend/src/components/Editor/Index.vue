<template>
    <vue-simplemde
        class="editor"
        :value="value"
        @input="$emit('input', $event)"
        :configs="configs"
        preview-class="markdown-body"
    />
</template>

<script>
import md from '@/utils/markdown';

export default {
    props: {
        value: String,
    },

    data: function() {
        return {
            configs: {
                autoDownloadFontAwesome: undefined,
                spellChecker: false,
                previewRender: function(text) {
                    return md.render(text);
                },
            },
        };
    },
};
</script>

<style lang="scss" scoped>
.editor {
    min-width: 0;
}
</style>

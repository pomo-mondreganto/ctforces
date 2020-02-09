<template>
    <vue-simplemde
        class="editor"
        v-model="content"
        :configs="configs"
        preview-class="markdown-body"
    />
</template>

<script>
import md from '@/utils/markdown';

export default {
    data: function() {
        return {
            content: '',
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

<template>
    <div class="group">
        <vue-simplemde
            class="editor"
            :value="value"
            @input="$emit('input', $event)"
            :configs="configs"
            preview-class="markdown-body"
        />
        <div v-if="invalid">
            <div v-for="error of errors" :key="error" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
import md from '@/utils/markdown';

export default {
    props: {
        value: String,
        errors: Array,
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

    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },
    },
};
</script>

<style lang="scss" scoped>
.editor {
    min-width: 0;
}

.error {
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

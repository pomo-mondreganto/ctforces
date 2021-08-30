<template>
    <div class="group">
        <vue-tags-input
            v-model="tag"
            :tags="value"
            :autocomplete-items="autocompleteTags"
            :max-tags="5"
            :maxlength="15"
            @tags-changed="
                newTags => {
                    $emit('input', newTags);
                }
            "
        />
        <div v-if="invalid">
            <div v-for="error of errors" :key="error" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
import VueTagsInput from '@johmun/vue-tags-input';

export default {
    data: function() {
        return {
            tag: '',
            autocompleteTags: [],
        };
    },

    props: {
        value: Array,
        errors: Array,
    },

    components: {
        VueTagsInput,
    },

    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },
    },

    watch: {
        tag: async function(currentTag) {
            if (currentTag.length == 0) {
                return;
            }
            try {
                const resp = await this.$http.get(
                    `/task_tags/?name=${currentTag}`
                );
                this.autocompleteTags = resp.data.results.map(value => {
                    return { text: value.name, id: value.id };
                });
            } catch (error) {
                this.autocompleteTags = [];
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.error {
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

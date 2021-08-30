<template>
    <div>
        <div class="task-buttons mb-2">
            <button class="btn green fb-0 fg-1" type="button" @click="add(0)">
                add
            </button>
            <div class="fb-0 fg-2" />
            <button
                class="btn disabled fb-0 fg-1"
                disabled
                type="button"
                @click="remove(0)"
            >
                remove
            </button>
        </div>
        <div v-for="(hint, index) of value" :key="index">
            <hint-item v-model="value[index]" />
            <div class="task-buttons mb-2">
                <button
                    class="btn green fb-0 fg-1"
                    type="button"
                    @click="add(index + 1)"
                >
                    add
                </button>
                <div class="fb-0 fg-2" />
                <button
                    class="btn red fb-0 fg-1"
                    type="button"
                    @click="remove(index)"
                >
                    remove
                </button>
            </div>
        </div>
        <div v-if="invalid">
            <div v-for="error of errors" :key="error" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
import HintItem from './HintListItem';

export default {
    props: {
        value: Array,
        errors: Array,
    },

    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },
    },

    methods: {
        add: function(index) {
            let hints = this.value.slice();
            hints.splice(index, 0, {
                body: null,
                is_published: false,
            });
            this.$emit('input', hints);
        },

        remove: function(index) {
            let hints = this.value.slice();
            hints.splice(index, 1);
            this.$emit('input', hints);
        },
    },

    components: {
        HintItem,
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

.task-buttons {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
}
</style>

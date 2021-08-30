<template>
    <div>
        <div class="task-buttons mb-2">
            <button type="button" class="btn green fb-0 fg-1" @click="add(0)">
                add
            </button>
            <div class="fb-0 fg-2" />
            <button
                type="button"
                class="btn disabled fb-0 fg-1"
                @click="remove(0)"
                disabled
            >
                remove
            </button>
        </div>
        <hr class="mb-2" />
        <div v-for="(task, index) of value" :key="task.idx">
            <task-list-item
                v-model="value[index]"
                :dynamicCost="dynamicScoring"
            />
            <div class="task-buttons mb-2">
                <button
                    type="button"
                    class="btn green fb-0 fg-1"
                    @click="add(index + 1)"
                >
                    add
                </button>
                <div class="fb-0 fg-2" />
                <button
                    type="button"
                    class="btn red fb-0 fg-1"
                    @click="remove(index)"
                >
                    remove
                </button>
            </div>
            <hr class="mb-2" />
        </div>
        <div v-if="invalid">
            <div v-for="(error, key) of errors" :key="key" class="error">
                {{ key }}: {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
import TaskListItem from './TaskListItem';

export default {
    props: {
        value: Array,
        errors: Object,
        dynamicScoring: Boolean,
    },

    components: {
        TaskListItem,
    },

    computed: {
        invalid: function() {
            return this.errors;
        },
    },

    methods: {
        add: function(index) {
            let tasks = this.value.slice();
            tasks.splice(index, 0, {
                id: null,
                name: null,
                cost: null,
                tags: [],
                mainTag: { name: null, id: null },
                idx: this._.uniqueId('task'),
            });
            this.$emit('input', tasks);
        },

        remove: function(index) {
            let tasks = this.value.slice();
            tasks.splice(index, 1);
            this.$emit('input', tasks);
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

.task-buttons {
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
}
</style>

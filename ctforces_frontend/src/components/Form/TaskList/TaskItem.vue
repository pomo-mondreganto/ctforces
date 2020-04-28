<template>
    <div>
        <div class="task">
            <div class="field">
                <f-input
                    type="text"
                    name="id"
                    :value="value.id"
                    @input="onChange"
                    placeholder="Id"
                    class="mr-1"
                />
            </div>
            <div class="field">
                <f-input
                    type="text"
                    name="name"
                    :value="value.name"
                    placeholder="Name"
                    disabled
                    class="mr-1"
                />
            </div>
            <div class="field">
                <f-input
                    type="text"
                    name="cost"
                    :value="value.cost"
                    @input="changeCost"
                    placeholder="Cost"
                    class="mr-1"
                    v-if="!$types.isNull(value.cost)"
                />
                <f-input
                    type="text"
                    name="cost"
                    :value="value.cost"
                    @input="changeCost"
                    placeholder="Cost"
                    class="mr-1"
                    disabled
                    v-else
                />
            </div>
            <div class="field vc">
                <f-select
                    :value="value.mainTag.name"
                    @input="changeMainTag"
                    :options="value.tags.map(({ name }) => name)"
                />
            </div>
        </div>
        <div class="ff mb-1">
            <f-detail :errors="errors['detail']" />
        </div>
    </div>
</template>

<script>
import FInput from '@/components/Form/Input';
import FSelect from '@/components/Form/Select';

export default {
    props: {
        value: Object,
        index: Number,
    },

    data: function() {
        return {
            errors: {},
        };
    },

    methods: {
        onChange: async function(id) {
            let newTask = { ...this.value };
            newTask['id'] = id;
            try {
                const r = await this.$http.get(`/tasks/${id}/`);
                const task = r.data;
                newTask['name'] = task.name;
                newTask['cost'] = task.cost.toString();
                newTask['tags'] = task.tags_details;
                newTask['mainTag'] = task.tags_details[0];
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                newTask['name'] = null;
                newTask['cost'] = null;
                newTask['tags'] = [];
                newTask['mainTag'] = { name: null, id: null };
            }
            this.$emit('input', newTask);
        },

        changeCost: function(cost) {
            this.$emit('input', { ...this.value, cost });
        },

        changeMainTag: function(mainTag) {
            let filtered = this.value.tags.filter(
                ({ name }) => name === mainTag
            );
            let tag = { name: null, id: null };
            if (filtered.length > 0) {
                tag = filtered[0];
            }
            this.$emit('input', {
                ...this.value,
                mainTag: tag,
            });
        },
    },

    components: {
        FInput,
        FSelect,
    },
};
</script>

<style lang="scss" scoped>
.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}

.task {
    display: flex;
    flex-flow: row nowrap;
}

.field {
    flex: 1 1 0;

    &.vc .group {
        flex: 1 1 0;
    }
}
</style>

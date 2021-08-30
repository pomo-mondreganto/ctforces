<template>
    <div>
        <div class="task">
            <div class="row">
                <div class="field">
                    <f-input
                        type="text"
                        name="id"
                        :value="value.id"
                        @input="searchTask"
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
                <div class="field" v-if="!dynamicCost">
                    <div>
                        <f-input
                            type="text"
                            name="cost"
                            :value="value.cost"
                            placeholder="Cost"
                            class="mr-1"
                            :disabled="disableFields"
                            @input="changeCost"
                        />
                    </div>
                </div>
                <div class="field">
                    <f-select
                        :value="value.mainTag.name"
                        :options="tagNames"
                        @input="changeMainTag"
                    />
                </div>
            </div>
            <div class="row mt-2" v-if="dynamicCost">
                <div class="field">
                    <f-input
                        type="text"
                        name="cost"
                        placeholder="Max cost"
                        class="mr-1"
                        :value="value.cost"
                        :disabled="disableFields"
                        @input="changeCost"
                    />
                </div>
                <div class="field">
                    <f-input
                        type="text"
                        name="min_cost"
                        placeholder="Min cost"
                        class="mr-1"
                        :value="value.minCost"
                        :disabled="disableFields"
                        @input="changeMinCost"
                    />
                </div>
                <div class="field">
                    <f-input
                        type="text"
                        name="decay"
                        placeholder="Decay"
                        :value="value.decay"
                        :disabled="disableFields"
                        @input="changeDecay"
                    />
                </div>
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
        dynamicCost: Boolean,
    },

    data: function() {
        return {
            errors: {},
        };
    },

    methods: {
        searchTask: async function(id) {
            let newTask = { ...this.value };
            newTask.id = id;
            try {
                const { data } = await this.$http.get(`/tasks/${id}/`);
                newTask.name = data.name;
                newTask.cost = data.cost.toString();
                newTask.minCost = '0';
                newTask.decay = '1';
                newTask.tags = data.tags_details;
                newTask.mainTag = data.tags_details[0];
                this.errors = {};
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                newTask.name = null;
                newTask.cost = null;
                newTask.minCost = null;
                newTask.decay = null;
                newTask.tags = [];
                newTask.mainTag = { name: null, id: null };
            }
            this.$emit('input', newTask);
        },

        changeCost: function(cost) {
            this.$emit('input', { ...this.value, cost });
        },

        changeMinCost: function(minCost) {
            this.$emit('input', { ...this.value, minCost });
        },

        changeDecay: function(decay) {
            this.$emit('input', { ...this.value, decay });
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

    computed: {
        tagNames: function() {
            return this.value.tags.map(({ name }) => name);
        },
        disableFields: function() {
            return this.$types.isNull(this.value.name);
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
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
}

.task {
    display: flex;
    flex-flow: column;
}

.row {
    display: flex;
    flex-flow: row nowrap;
}

.field {
    flex: 1;
}
</style>

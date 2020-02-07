<template>
    <div class="table">
        <div class="table-head">
            <div
                v-for="field of fields"
                :key="field.name"
                :class="header({ grow: field.grow, pos: field.pos })"
                class="table-head-col"
            >
                {{ field.name }}
            </div>
        </div>
        <div class="table-body">
            <div class="table-row" v-for="(row, index) of data" :key="index">
                <div
                    v-for="field of fields"
                    :key="field.name"
                    :class="header({ grow: field.grow, pos: field.pos })"
                    class="table-body-col"
                >
                    <component
                        :is="getComponent(field)"
                        :row="row"
                        :field="row[getFieldName(field)]"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { isUndefined } from '@/utils/types';
import Text from './Text';

export default {
    props: {
        fields: Array,
        data: Array,
    },
    methods: {
        getComponent: function(field) {
            if (!isUndefined(field.comp)) {
                return field.comp;
            } else {
                return Text;
            }
        },
        getFieldName: function(field) {
            if (!isUndefined(field.key)) {
                return field.key;
            } else {
                return field.name.toLowerCase();
            }
        },
        getPos: function(pos) {
            if (!isUndefined(pos)) {
              return `jc-${pos}`;
            }
        },
        header: function({ grow = 1, pos = 'c' }) {
            return ['ai-c', 'fb-0', `fg-${grow}`, this.getPos(pos)];
        },
    },
};
</script>

<style lang="scss" scoped>
.table {
    display: flex;
    flex-flow: column nowrap;
}

.table-head {
    display: flex;
    flex-flow: row nowrap;
    background-color: $gray;
    border-top-right-radius: 0.5em;
    border-top-left-radius: 0.5em;
}

.table-head-col {
    padding: 0.8em;
    display: flex;
}

.table-body {
    display: flex;
    flex-flow: column nowrap;
}

.table-row {
    display: flex;
    flex-flow: row nowrap;
    border-bottom: 0.05em solid $gray;

    .table-body-col {
        padding: 0.8em;
        border-right: 0.05em solid $gray;
        display: flex;

        &:nth-child(1) {
            border-left: 0.05em solid $gray;
        }
    }
}
</style>

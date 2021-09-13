<template>
    <div class="mt-1">
        <f-table
            :fields="[
                { name: '#', pos: 'c', grow: 1 },
                {
                    name: 'Name',
                    pos: 'l',
                    grow: 7,
                    comp: TaskLinkComp,
                },
                { name: 'Cost', grow: 2 },
                {
                    name: 'Tags',
                    grow: 5,
                    key: 'task_tags_details',
                    comp: TagsComp,
                },
                {
                    name: 'Solved',
                    grow: 2,
                    key: 'solved_count',
                    comp: TaskSolvedLinkComp,
                },
            ]"
            :data="tasks"
        />
    </div>
</template>

<script>
import Tags from './Tags';
import TaskLink from './Link';
import TaskSolvedLink from './SolvedLink';
import FTable from '@/components/Table/Index';

export default {
    props: {
        tasks: Array,
    },
    components: {
        FTable,
    },
    data: function() {
        return {
            TagsComp: Tags,
            TaskLinkComp: TaskLink,
            TaskSolvedLinkComp: TaskSolvedLink,
        };
    },
};
</script>

<style></style>

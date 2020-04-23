<template>
    <master-layout>
        <card>
            <div
                class="p-r"
                v-if="!$types.isNull(user) && user.can_create_tasks"
            >
                <div class="a-tr">
                    <router-link :to="{ name: 'task_create' }" class="btn nlnk">
                        Create task
                    </router-link>
                </div>
            </div>
            <f-header text="Tasks" />
            <div class="mt-1" v-if="!$types.isNull(tasks)">
                <f-table
                    :fields="[
                        { name: '#', pos: 'c', grow: 1 },
                        {
                            name: 'Name',
                            pos: 'l',
                            grow: 7,
                            comp: TaskLinkComp,
                        },
                        { name: 'Cost', grow: 1 },
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
            <f-detail :errors="errors['detail']" />
            <pagination :count="count" :pagesize="pagesize" />
        </card>
        <template v-slot:sidebar>
            <div>123</div>
        </template>
    </master-layout>
</template>

<script>
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import Tags from './TaskTags';
import TaskLink from './TaskLink';
import TaskSolvedLink from './TaskSolvedLink';
import Pagination from '@/components/Pagination/Index';
import { mapState } from 'vuex';

export default {
    components: {
        FHeader,
        FTable,
        Pagination,
    },

    data: function() {
        return {
            tasks: null,
            TagsComp: Tags,
            TaskLinkComp: TaskLink,
            TaskSolvedLinkComp: TaskSolvedLink,
            errors: {},
            count: null,
            pagesize: 30,
        };
    },

    created: async function() {
        await this.fetchTasks();
    },

    watch: {
        async $route() {
            await this.fetchTasks();
        },
    },

    methods: {
        fetchTasks: async function() {
            const { page = 1 } = this.$route.query;
            try {
                const r = await this.$http.get(
                    `/tasks/?page=${page}&page_size=${this.pagesize}`
                );
                this.tasks = r.data.results.map((row, index) => {
                    return {
                        '#': 1 + index + (page - 1) * this.pagesize,
                        ...row,
                    };
                });
                this.count = r.data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: mapState(['user']),
};
</script>

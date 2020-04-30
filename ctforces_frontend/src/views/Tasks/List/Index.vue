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
            <f-detail :errors="errors['detail']" />
            <pagination :count="count" :pagesize="pagesize" />
        </card>
        <template v-slot:sidebar>
            <sidebar>
                <template v-slot:top>
                    <card class="mb-2">
                        <div class="sidebar-header ta-c">Search</div>
                        <div class="ff">
                            <f-input
                                type="text"
                                name="search"
                                v-model="search"
                                placeholder="Search"
                            />
                        </div>
                    </card>
                </template>
            </sidebar>
        </template>
    </master-layout>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import Tags from './TaskTags';
import TaskLink from './TaskLink';
import TaskSolvedLink from './TaskSolvedLink';
import Pagination from '@/components/Pagination/Index';
import Sidebar from '@/components/Sidebar/Index';
import { mapState } from 'vuex';

export default {
    components: {
        FInput,
        FHeader,
        FTable,
        Pagination,
        Sidebar,
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
            search: null,
        };
    },

    created: async function() {
        const { search = null } = this.$route.query;
        this.search = search;
        await this.fetchTasks();
    },

    watch: {
        search: async function(value) {
            if (this.$types.isString(value) && value.length > 0) {
                const query = Object.assign({}, this.$route.query, {
                    page: 1,
                    search: value,
                });
                this.$router.push({ query }).catch(() => {});
            } else {
                const query = Object.assign({}, this.$route.query, {
                    page: 1,
                    search: undefined,
                });
                this.$router.push({ query }).catch(() => {});
            }
        },

        async $route() {
            await this.fetchTasks();
        },
    },

    methods: {
        fetchTasks: async function() {
            const { search = null, tag = null, page = 1 } = this.$route.query;
            try {
                let r;
                if (!this.$types.isNull(tag)) {
                    r = await this.$http.get(
                        `/tasks/?tag=${tag}&page=${page}&page_size=${this.pagesize}`
                    );
                } else if (this.$types.isNull(search)) {
                    r = await this.$http.get(
                        `/tasks/?page=${page}&page_size=${this.pagesize}`
                    );
                } else {
                    r = await this.$http.get(
                        `/tasks/?q=${search}&page=${page}&page_size=${this.pagesize}`
                    );
                }

                this.tasks = r.data.results.map((row, index) => {
                    return {
                        '#': 1 + index + (page - 1) * this.pagesize,
                        customClasses: row.is_solved_by_user ? ['solved'] : [],
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

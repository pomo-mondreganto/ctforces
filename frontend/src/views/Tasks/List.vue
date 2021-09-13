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
            <task-list :tasks="tasks" v-if="!$types.isNull(tasks)" />
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
import TaskList from '@/components/Tasks/List';
import Pagination from '@/components/Pagination';
import Sidebar from '@/components/Sidebar';
import { mapState } from 'vuex';

export default {
    components: {
        FInput,
        FHeader,
        Pagination,
        Sidebar,
        TaskList,
    },

    data: function() {
        return {
            tasks: null,
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
                const params = {
                    page: page,
                    page_size: this.pagesize,
                };
                if (!this.$types.isNull(tag)) {
                    params['tag'] = tag;
                } else if (!this.$types.isNull(search)) {
                    params['q'] = search;
                }
                const { data } = await this.$http.get(`/tasks/`, { params });

                this.tasks = data.results.map((row, index) => {
                    return {
                        '#': 1 + index + (page - 1) * this.pagesize,
                        customClasses: row.is_solved_by_user ? ['solved'] : [],
                        ...row,
                    };
                });
                this.count = data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: mapState(['user']),
};
</script>

<template>
    <div class="p-r">
        <div class="a-tr" v-if="showCreateButton">
            <router-link :to="{ name: 'team_create' }" class="btn nlnk">
                Create task
            </router-link>
        </div>
        <f-header :text="`${$route.params.username} tasks`" />
        <task-list :tasks="tasks" v-if="!$types.isNull(tasks)" />
        <f-detail :errors="errors['detail']" />
        <pagination :count="count" :pagesize="pagesize" />
    </div>
</template>

<script>
import FHeader from '@/components/Form/Header';
import { mapState } from 'vuex';
import Pagination from '@/components/Pagination';
import TaskList from '@/components/Tasks/List';

export default {
    components: {
        FHeader,
        Pagination,
        TaskList,
    },

    data: function() {
        return {
            tasks: null,
            errors: {},
            count: null,
            pagesize: 30,
        };
    },

    methods: {
        fetchTasks: async function() {
            const { page = 1 } = this.$route.query;
            const params = {
                page: page,
                page_size: this.pagesize,
            };
            try {
                const {
                    data,
                } = await this.$http.get(
                    `/users/${this.$route.params.username}/tasks/`,
                    { params }
                );
                this.tasks = data.results.map((task, index) => {
                    return {
                        '#': 1 + index + (page - 1) * this.pagesize,
                        ...task,
                    };
                });
                this.count = data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchTasks();
    },

    computed: {
        ...mapState(['user']),
        showCreateButton: function() {
            return (
                !this.$types.isNull(this.user) &&
                this.user.username === this.$route.params.username &&
                this.user.can_create_tasks
            );
        },
    },

    watch: {
        async $route() {
            await this.fetchTasks();
        },
    },
};
</script>

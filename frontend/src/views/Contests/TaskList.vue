<template>
    <div>
        <div
            class="p-r"
            v-if="!$types.isNull(contest) && contest.can_edit_contest"
        >
            <div class="a-tr">
                <router-link
                    :to="{ name: 'contest_edit', params: { id: contest.id } }"
                    class="btn nlnk"
                >
                    Edit contest
                </router-link>
            </div>
        </div>
        <task-view :contest="contest" :contest_tasks="contest_tasks" />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import TaskView from '@/components/Contests/TaskView.vue';
import { mapState } from 'vuex';

export default {
    data: function() {
        return {
            contest_tasks: null,
            errors: {},
        };
    },

    components: {
        TaskView,
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
            const { id } = this.$route.params;
            try {
                const { data } = await this.$http.get(`/contests/${id}/tasks/`);
                this.contest_tasks = data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: mapState('contests', ['contest']),
};
</script>

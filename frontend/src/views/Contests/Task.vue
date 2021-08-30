<template>
    <div>
        <task
            :task="task"
            :errors="serrors"
            :submitFlag="submit"
            :solved="solved"
        />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import Task from '@/components/Tasks/View';
import { mapState } from 'vuex';

export default {
    components: {
        Task,
    },

    created: async function() {
        await this.fetchTask();
    },

    data: function() {
        return {
            task: null,
            errors: {},
            serrors: {},
            solved: {},
        };
    },

    watch: {
        async $route() {
            await this.fetchTask();
        },
    },

    methods: {
        fetchTask: async function() {
            const { id, task_id } = this.$route.params;
            try {
                const r = await this.$http.get(
                    `/contests/${id}/tasks/${task_id}/`
                );
                this.task = r.data;
                this.solved = {
                    number: this.task.solved_count,
                    link: this.contest.can_view_scoreboard
                        ? {
                              name: 'contest_task_solved',
                              params: { id, task_id },
                          }
                        : null,
                };
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        submit: async function(flag) {
            const { id, task_id } = this.$route.params;
            try {
                const { data } = await this.$http.post(
                    `/contests/${id}/tasks/${task_id}/submit/`,
                    {
                        flag: flag,
                    }
                );
                this.$toasted.success('Valid flag!');
                this.serrors = {};
                if (data.upsolving) {
                    this.$set(this.task, 'is_solved_on_upsolving', true);
                    this.$toasted.info(
                        'Contest is finished. Points will be added to upsolving.'
                    );
                } else {
                    this.$set(this.task, 'is_solved_by_user', true);
                }
            } catch (error) {
                this.serrors = this.$parse(error.response.data);
                if (
                    !this.$types.isUndefined(this.serrors['flag']) &&
                    this.serrors['flag'].length > 0 &&
                    this.serrors['flag'][0] === 'Invalid flag.'
                ) {
                    this.$toasted.error('Invalid flag!');
                }
            }
        },
    },

    computed: mapState('contests', ['contest']),
};
</script>

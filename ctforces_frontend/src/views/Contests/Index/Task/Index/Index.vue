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
import Task from '@/components/Task/Index';

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
                    link: {
                        name: 'contest_task_solved',
                        params: { id, task_id },
                    },
                };
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        submit: async function(flag) {
            const { id, task_id } = this.$route.params;
            try {
                await this.$http.post(
                    `/contests/${id}/tasks/${task_id}/submit/`,
                    {
                        flag: flag,
                    }
                );
                this.$toasted.success('Valid flag!');
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
};
</script>

<template>
    <master-layout>
        <contest-form
            text="Create contest"
            :initialTasks="[]"
            :errors="errors"
            @submit="createContest"
        />
    </master-layout>
</template>

<script>
import ContestForm from '@/components/Contests/Form';

export default {
    components: {
        ContestForm,
    },

    data: function() {
        return {
            errors: {},
        };
    },

    methods: {
        createContest: async function({ contest, tasks }) {
            let data = null;
            try {
                const resp = await this.$http.post(
                    `/contests/`,
                    contest.dumpForAPI()
                );
                data = resp.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                return;
            }

            const ctrsToCreate = tasks.map(task => {
                return {
                    task: task.id,
                    contest: data.id,
                    cost: task.cost,
                    min_cost: task.minCost,
                    decay_value: task.decay,
                    main_tag: task.mainTag.id,
                };
            });

            try {
                await this.$http.post(
                    '/contest_task_relationship/',
                    ctrsToCreate
                );
                this.$router.push({
                    name: 'contest_tasks',
                    params: { id: data.id },
                });
            } catch {
                this.$router.push({
                    name: 'contest_edit',
                    params: { id: data.id },
                });
            }
        },
    },
};
</script>

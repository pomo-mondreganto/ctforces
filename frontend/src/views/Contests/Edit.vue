<template>
    <master-layout>
        <contest-form
            text="Edit contest"
            :key="initialContest.id"
            :initialContest="initialContest"
            :initialTasks="initialTasks"
            :errors="errors"
            @submit="editContest"
        />
    </master-layout>
</template>

<script>
import ContestForm from '@/components/Form/Contest';
import Contest from '@/models/contest';

export default {
    components: {
        ContestForm,
    },

    data: function() {
        return {
            initialContest: new Contest(),
            initialTasks: [],
            oldTasks: {},
            errors: {},
        };
    },

    created: async function() {
        await this.fetchData();
    },

    methods: {
        fetchData: async function() {
            const { id } = this.$route.params;
            try {
                const { data } = await this.$http.get(`/contests/${id}/full/`);
                this.initialContest = new Contest(data);
                const self = this;
                this.initialTasks = data.contest_task_relationship_details.map(
                    ctr => {
                        self.oldTasks[ctr.task] = ctr.id;
                        return {
                            cost: ctr.cost.toString(),
                            minCost: ctr.min_cost.toString(),
                            decay: ctr.decay_value.toString(),
                            id: ctr.task.toString(),
                            name: ctr.task_details.name,
                            mainTag: ctr.main_tag_details,
                            tags: ctr.task_details.task_tags_details,
                        };
                    }
                );
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        editContest: async function({ contest, tasks }) {
            const { id: cid } = this.$route.params;
            let data = null;
            try {
                const resp = await this.$http.put(
                    `/contests/${cid}/`,
                    contest.dumpForAPI()
                );
                data = resp.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                return;
            }

            try {
                let newTasks = {};
                for (const task of tasks) {
                    newTasks[task.id] = true;
                    const changes = {
                        min_cost: task.minCost,
                        decay_value: task.decay,
                        cost: task.cost,
                        main_tag: task.mainTag.id,
                    };

                    if (this.oldTasks[task.id]) {
                        await this.$http.patch(
                            `/contest_task_relationship/${
                                this.oldTasks[task.id]
                            }/`,
                            changes
                        );
                    } else {
                        await this.$http.post('/contest_task_relationship/', {
                            ...changes,
                            task: task.id,
                            contest: data.id,
                        });
                    }
                }

                for (const id in this.oldTasks) {
                    if (newTasks[id]) {
                        continue;
                    }
                    await this.$http.delete(
                        `/contest_task_relationship/${this.oldTasks[id]}/`
                    );
                }

                this.$router.push({
                    name: 'contest_tasks',
                    params: { id: cid },
                });
            } catch (error) {
                this.errors = { tasks: this.$parse(error.response.data) };
                await this.fetchData();
            }
        },
    },
};
</script>

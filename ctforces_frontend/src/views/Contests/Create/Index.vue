<template>
    <master-layout>
        <card>
            <f-header header text="Create contest"></f-header>
            <form class="mt-2" @submit.prevent="createContest">
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="name"
                        v-model="name"
                        :errors="errors['name']"
                        placeholder="Name"
                    />
                </div>
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="description"
                        v-model="description"
                        :errors="errors['description']"
                        placeholder="Description"
                    />
                </div>
                <div class="ff">
                    <f-task-list v-model="tasks" :errors="errors['tasks']" />
                </div>
                <div class="ff">
                    <f-checkbox
                        name="is_published"
                        v-model="isPublished"
                        label="Published"
                        :errors="errors['is_published']"
                    />
                </div>
                <div class="ff">
                    <f-checkbox
                        name="is_registration_open"
                        v-model="isRegistrationOpen"
                        label="Registration is opened"
                        :errors="errors['is_registration_open']"
                    />
                </div>
                <div class="ff">
                    <f-checkbox
                        name="is_rated"
                        v-model="isRated"
                        label="Rated"
                        :errors="errors['is_rated']"
                    />
                </div>
                <div class="ff">
                    <f-checkbox
                        name="publish_tasks_after_finished"
                        v-model="publishTasksAfterFinished"
                        label="Publish tasks after finish"
                        :errors="errors['publish_tasks_after_finished']"
                    />
                </div>
                <div class="ff">
                    <f-datetime
                        label="Start time"
                        v-model="startTime"
                        :errors="errors['start_time']"
                    />
                </div>
                <div class="ff">
                    <f-datetime
                        label="End time"
                        v-model="endTime"
                        :errors="errors['end_time']"
                    />
                </div>
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Create" class="btn" />
                </div>
            </form>
        </card>
    </master-layout>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FCheckbox from '@/components/Form/Checkbox';
import FTaskList from '@/components/Form/TaskList/Index';
import FDatetime from '@/components/Form/Datetime';

export default {
    data: function() {
        return {
            name: null,
            description: null,
            tasks: [],
            isPublished: false,
            isRegistrationOpen: false,
            isRated: false,
            publishTasksAfterFinished: false,
            startTime: null,
            endTime: null,
            errors: {},
        };
    },

    methods: {
        createContest: async function() {
            try {
                const r = await this.$http.post(`/contests/`, {
                    name: this.name,
                    description: this.description,
                    is_published: this.isPublished,
                    is_registration_open: this.isRegistrationOpen,
                    is_rated: this.isRated,
                    publish_tasks_after_finished: this
                        .publishTasksAfterFinished,
                    start_time: new Date(this.startTime).toISOString(),
                    end_time: new Date(this.endTime).toISOString(),
                });

                for (const [i, task] of this.tasks.entries()) {
                    await this.$http.post('/contest_task_relationship/', {
                        task: parseInt(task.id, 10),
                        contest: r.data.id,
                        ordering_number: i,
                        cost: task.cost,
                        main_tag: parseInt(task.mainTag, 10),
                    });
                }

                this.$router.push({
                    name: 'contest_tasks',
                    params: { id: r.data.id },
                });
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    components: {
        FInput,
        FHeader,
        FCheckbox,
        FTaskList,
        FDatetime,
    },
};
</script>

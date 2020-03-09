<template>
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
                    name="is_running"
                    v-model="isRunning"
                    label="Running"
                    :errors="errors['is_running']"
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
                <f-checkbox
                    name="is_finished"
                    v-model="isFinished"
                    label="Finished"
                    :errors="errors['is_finished']"
                />
            </div>
            <div class="ff">
                <f-datetime
                    label="Start time"
                    v-model="start_time"
                    :errors="errors['start_time']"
                />
            </div>
            <div class="ff">
                <f-datetime
                    label="End time"
                    v-model="end_time"
                    :errors="errors['end_time']"
                />
            </div>
            <div class="ff">
                <input type="submit" value="Create" class="btn" />
            </div>
        </form>
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
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
            isRunning: false,
            publishTasksAfterFinished: false,
            isFinished: false,
            start_time: null,
            end_time: null,
            errors: {},
        };
    },

    methods: {
        createContest: async function() {
            try {
                const r = await this.$http.post(`/contests/`, {
                    name: this.name,
                    description: this.description,
                    tasks: this.tasks.map(({ id, name, cost, main_tag }) => ({
                        id: parseInt(id, 10),
                        name,
                        cost: parseInt(cost, 10),
                        main_tag: parseInt(main_tag, 10),
                    })),
                    is_published: this.isPublished,
                    is_registration_open: this.isRegistrationOpen,
                    is_rated: this.isRated,
                    is_running: this.isRunning,
                    publish_tasks_after_finished: this
                        .publishTasksAfterFinished,
                    is_finished: this.isFinished,
                    start_time: this.start_time,
                    end_time: this.end_time,
                });
                console.log(r);
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    components: {
        Card,
        FInput,
        FHeader,
        FCheckbox,
        FTaskList,
        FDatetime,
    },
};
</script>

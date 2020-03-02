<template>
    <card>
        <f-header header text="Create contest"></f-header>
        <form class="def-form mt-2" @submit.prevent="createContest">
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="name"
                    v-model="name"
                    :errors="errors['name']"
                    placeholder="Name"
                ></f-input>
            </div>
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="description"
                    v-model="description"
                    :errors="errors['description']"
                    placeholder="Description"
                ></f-input>
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_published"
                    v-model="isPublished"
                    label="Published"
                    :errors="errors['is_published']"
                ></f-checkbox>
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_registration_open"
                    v-model="isRegistrationOpen"
                    label="Registration is opened"
                    :errors="errors['is_registration_open']"
                ></f-checkbox>
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_rated"
                    v-model="isRated"
                    label="Rated"
                    :errors="errors['is_rated']"
                ></f-checkbox>
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_running"
                    v-model="isRunning"
                    label="Running"
                    :errors="errors['is_running']"
                ></f-checkbox>
            </div>
            <div class="ff">
                <f-checkbox
                    name="publish_tasks_after_finished"
                    v-model="publishTasksAfterFinished"
                    label="Publish tasks after finish"
                    :errors="errors['publish_tasks_after_finished']"
                ></f-checkbox>
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_finished"
                    v-model="isFinished"
                    label="Finished"
                    :errors="errors['is_finished']"
                ></f-checkbox>
            </div>
        </form>
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FCheckbox from '@/components/Form/Checkbox';

export default {
    data: function() {
        return {
            name: null,
            description: null,
            isPublished: false,
            isRegistrationOpen: false,
            isRated: false,
            isRunning: false,
            publishTasksAfterFinished: false,
            isFinished: false,
            start_time: null,
            errors: {},
        };
    },

    methods: {
        createContest: async function() {},
    },

    components: {
        Card,
        FInput,
        FHeader,
        FCheckbox,
    },
};
</script>

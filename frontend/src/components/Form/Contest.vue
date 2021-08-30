<template>
    <card>
        <f-header header :text="text"></f-header>
        <form
            class="mt-2"
            @submit.prevent="$emit('submit', { contest, tasks })"
        >
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="name"
                    v-model="contest.name"
                    :errors="errors.name"
                    placeholder="Name"
                />
            </div>
            <div class="ff">
                <editor
                    v-model="contest.description"
                    :errors="errors.description"
                />
            </div>
            <hr class="mt-2" />
            <div class="ff">
                <f-checkbox
                    name="dynamic_scoring"
                    v-model="contest.dynamic_scoring"
                    label="Dynamic scoring"
                    :errors="errors.dynamic_scoring"
                />
            </div>
            <div class="ff">
                <f-task-list
                    v-model="tasks"
                    :dynamicScoring="contest.dynamic_scoring"
                    :errors="errors.tasks"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_published"
                    v-model="contest.is_published"
                    label="Published"
                    :errors="errors.is_published"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_registration_open"
                    v-model="contest.is_registration_open"
                    label="Registration is opened"
                    :errors="errors.is_registration_open"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_rated"
                    v-model="contest.is_rated"
                    label="Rated"
                    :errors="errors.is_rated"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="always_recalculate_rating"
                    v-model="contest.always_recalculate_rating"
                    label="Always recalculate rating"
                    :errors="errors.always_recalculate_rating"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="publish_tasks_after_finished"
                    v-model="contest.publish_tasks_after_finished"
                    label="Publish tasks after finish"
                    :errors="errors.publish_tasks_after_finished"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="public_scoreboard"
                    v-model="contest.public_scoreboard"
                    label="Public scoreboard"
                    :errors="errors.public_scoreboard"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="is_virtual"
                    v-model="contest.is_virtual"
                    label="Virtual"
                    :errors="errors.is_virtual"
                />
            </div>
            <div v-if="contest.is_virtual" class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="virtual_duration"
                    v-model="contest.virtual_duration"
                    :errors="errors.virtual_duration"
                    placeholder="Virtual duration ([DD] [HH:[MM:]]ss[.uuuuuu])"
                />
            </div>
            <div class="ff">
                <f-datetime
                    label="Start time"
                    v-model="contest.start_time"
                    :errors="errors.start_time"
                />
            </div>
            <div class="ff">
                <f-datetime
                    label="End time"
                    v-model="contest.end_time"
                    :errors="errors.end_time"
                />
            </div>
            <div class="ff">
                <f-detail :errors="errors.detail" />
            </div>
            <div class="ff">
                <input type="submit" value="Submit" class="btn" />
            </div>
        </form>
    </card>
</template>

<script>
import Editor from '@/components/Editor';
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FCheckbox from '@/components/Form/Checkbox';
import FTaskList from '@/components/Form/TaskList';
import FDatetime from '@/components/Form/Datetime';
import Contest from '@/models/contest';

export default {
    props: {
        text: String,
        initialContest: Object,
        initialTasks: Array,
        errors: Object,
    },

    data: function() {
        return {
            contest: this.initialContest ?? new Contest(),
            tasks: this.initialTasks,
        };
    },

    components: {
        Editor,
        FInput,
        FHeader,
        FCheckbox,
        FTaskList,
        FDatetime,
    },
};
</script>

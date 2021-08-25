<template>
    <master-layout>
        <card>
            <f-header header text="Edit contest"></f-header>
            <form class="mt-2" @submit.prevent="editContest">
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
                    <editor
                        v-model="description"
                        :errors="errors['description']"
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
                    <f-checkbox
                        name="public_scoreboard"
                        v-model="publicScoreboard"
                        label="Public scoreboard"
                        :errors="errors['public_scoreboard']"
                    />
                </div>
                <div class="ff">
                    <f-checkbox
                        name="dynamic_scoring"
                        v-model="dynamicScoring"
                        label="Dynamic scoring"
                        :errors="errors['dynamic_scoring']"
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
                    <input type="submit" value="Edit" class="btn" />
                </div>
            </form>
        </card>
    </master-layout>
</template>

<script>
import Editor from '@/components/Editor';
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FCheckbox from '@/components/Form/Checkbox';
import FTaskList from '@/components/Form/TaskList';
import FDatetime from '@/components/Form/Datetime';

export default {
    data: function() {
        return {
            name: null,
            description: null,
            tasks: [],
            oldTasks: {},
            isPublished: false,
            isRegistrationOpen: false,
            isRated: false,
            publishTasksAfterFinished: false,
            publicScoreboard: false,
            dynamicScoring: false,
            startTime: null,
            endTime: null,
            errors: {},
        };
    },

    created: async function() {
        const { id } = this.$route.params;
        try {
            const { data } = await this.$http.get(`/contests/${id}/full/`);
            this.name = data.name;
            this.description = data.description;
            this.isPublished = data.is_published;
            this.isRegistrationOpen = data.is_registration_open;
            this.isRated = data.is_rated;
            this.publishTasksAfterFinished = data.publish_tasks_after_finished;
            this.publicScoreboard = data.public_scoreboard;
            this.dynamicScoring = data.dynamic_scoring;
            this.startTime = data.start_time;
            this.endTime = data.end_time;
            let self = this;
            this.tasks = data.contest_task_relationship_details.map(ctr => {
                self.oldTasks[ctr.task.id] = ctr.id;
                return {
                    cost: ctr.cost.toString(),
                    id: ctr.task.toString(),
                    name: ctr.task_details.name,
                    mainTag: ctr.main_tag_details,
                    tags: ctr.task_details.task_tags_details,
                };
            });
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },

    methods: {
        editContest: async function() {
            const { id: cid } = this.$route.params;
            try {
                const r = await this.$http.put(`/contests/${cid}/`, {
                    name: this.name,
                    description: this.description,
                    is_published: this.isPublished,
                    is_registration_open: this.isRegistrationOpen,
                    is_rated: this.isRated,
                    publish_tasks_after_finished: this
                        .publishTasksAfterFinished,
                    public_scoreboard: this.publicScoreboard,
                    dynamic_scoring: this.dynamicScoring,
                    start_time: new Date(this.startTime).toISOString(),
                    end_time: new Date(this.endTime).toISOString(),
                });

                let newTasks = {};

                for (const task of this.tasks) {
                    newTasks[task.id] = true;
                    if (this.oldTasks[task.id]) {
                        await this.$http.put(
                            `/contest_task_relationship/${
                                this.oldTasks[task.id]
                            }/`,
                            {
                                task: parseInt(task.id, 10),
                                contest: r.data.id,
                                cost: parseInt(task.cost, 10),
                                main_tag: parseInt(task.mainTag.id, 10),
                            }
                        );
                    } else {
                        await this.$http.post('/contest_task_relationship/', {
                            task: parseInt(task.id, 10),
                            contest: r.data.id,
                            cost: parseInt(task.cost, 10),
                            main_tag: parseInt(task.mainTag.id, 10),
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
                this.errors = this.$parse(error.response.data);
            }
        },
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

<template>
    <div v-if="!$types.isNull(contest)">
        <div
            class="mt-1"
            v-for="taskRow in tasks"
            :key="taskRow[0].main_tag_details.id"
        >
            <div class="task-tag mb-1">
                {{ taskRow[0].main_tag_details.name }}
            </div>
            <div class="tasks">
                <div
                    class="task-wrap"
                    v-for="(task, index) of taskRow"
                    :key="index"
                    @click="openTask(task.task)"
                >
                    <div class="task">
                        <div class="name">
                            {{ task.task_name }}
                        </div>
                        <div class="cost">
                            {{ task.cost }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        contest: Object,
        errors: Object,
    },

    computed: {
        tasks: function() {
            if (this.$types.isNull(this.contest)) {
                return null;
            }
            return this._.groupBy(
                this.contest.contest_task_relationship_details,
                ({ main_tag_details: { name } }) => name
            );
        },
    },

    methods: {
        openTask: function(task) {
            this.$router
                .push({
                    name: 'contest_task',
                    params: { task_id: task },
                })
                .catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.task-tag {
    font-size: 1.3em;
}

.tasks {
    display: flex;
    flex-flow: row wrap;
    justify-content: left;
}

.task-wrap {
    cursor: pointer;
    flex: 0 1 auto;
    min-width: 13em;
    border: 0.05em solid rgba($darklight, 0.5);
    border-radius: 0.4em;
    margin-right: 1em;
    margin-bottom: 1em;
    background-color: rgba($bluelight, 0.3);
}

.task {
    text-align: center;
    padding-bottom: 5%;
    padding-top: 5%;
}

.name {
    margin-top: 0.5em;
}

.cost {
    margin-top: 1em;
    margin-bottom: 0.5em;
}
</style>

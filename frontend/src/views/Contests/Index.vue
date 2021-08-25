<template>
    <master-layout-stacked>
        <tabs :tabs="tabs">
            <router-view />
        </tabs>
        <template v-slot:sidebar>
            <div>
                <card class="pl-2" v-if="!$types.isNull(contest)">
                    <div class="header">
                        {{ contest.name }}
                    </div>
                    <div class="author mt-1 mb-2">
                        By
                        <user
                            :username="contest.author_username"
                            :rating="contest.author_rating"
                        />
                    </div>
                    <div v-if="contest.is_running">
                        Contest is <span class="running">running</span>
                        <div class="mt-1">
                            <countdown
                                :time="new Date(contest.end_time) - new Date()"
                            >
                                <template v-slot="props">
                                    <span class="countdown-more"
                                        >Time Remaining：</span
                                    >
                                    <span class="countdown">{{
                                        $time(props.time)
                                    }}</span>
                                </template>
                            </countdown>
                        </div>
                    </div>
                    <div v-else-if="contest.is_finished">
                        Contest is <span class="finished">finished</span>
                    </div>
                    <div v-else>
                        Contest is <span class="upcoming">upcoming</span>
                        <div class="mt-1">
                            <countdown
                                :time="
                                    new Date(contest.start_time) - new Date()
                                "
                                v-slot="props"
                            >
                                <span class="countdown-more">Starts in </span>
                                <span class="countdown">{{
                                    $time(props.time)
                                }}</span>
                            </countdown>
                        </div>
                    </div>
                    <div class="mt-1">
                        Scoring is <span class="scoring">{{ scoring }}</span>
                    </div>
                    <f-detail :errors="errors['detail']" />
                </card>
            </div>
        </template>
    </master-layout-stacked>
</template>

<script>
import Tabs from '@/components/Tabs';

export default {
    components: {
        Tabs,
    },

    data: function() {
        return {
            contest: null,
            errors: {},
        };
    },

    created: async function() {
        await this.fetchContest();
    },

    watch: {
        async $route() {
            await this.fetchContest();
        },
    },

    methods: {
        fetchContest: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/contests/${id}/`);
                this.contest = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: {
        tabs: function() {
            const result = [
                {
                    name: 'Tasks',
                    to: {
                        name: 'contest_tasks',
                        params: { id: this.$route.params.id },
                    },
                },
            ];
            if (this.contest && this.contest.can_view_scoreboard) {
                result.push({
                    name: 'Scoreboard',
                    to: {
                        name: 'contest_scoreboard',
                        params: { id: this.$route.params.id },
                    },
                });
            }
            return result;
        },
        scoring: function() {
            return this.contest.dynamic_scoring ? 'dynamic' : 'static';
        },
    },
};
</script>

<style lang="scss" scoped>
.upcoming {
    @include use-theme {
        color: $reddanger;
    }
}

.running {
    @include use-theme {
        color: $green;
    }
}

.scoring {
    font-weight: 900;
}

.header {
    font-size: 2em;
}

@media only screen and (max-width: 1199px) {
    .countdown-more {
        display: none;
    }
}
</style>

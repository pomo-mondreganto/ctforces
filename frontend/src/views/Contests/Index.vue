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
                    <div v-if="contestState.status == 'RUNNING'">
                        Contest is
                        <span class="running"
                            >running
                            {{ contest.is_virtual ? 'virtually' : '' }}</span
                        >
                        <div class="mt-1">
                            <countdown :time="contestState.time">
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
                    <div v-else-if="contestState.status == 'FINISHED'">
                        Contest is <span class="finished">finished</span>
                        {{
                            contest.is_virtual && !contest.is_finished
                                ? 'for your team'
                                : ''
                        }}
                    </div>
                    <div v-else-if="contestState.status == 'UPCOMING'">
                        Contest is <span class="upcoming">upcoming</span>
                        <div class="mt-1">
                            <countdown :time="contestState.time" v-slot="props">
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
import moment from 'moment';
import { mapState, mapActions } from 'vuex';

export default {
    components: {
        Tabs,
    },

    created: async function() {
        await this.fetchContest(this.contestID);
    },

    watch: {
        async $route() {
            await this.fetchContest(this.contestID);
        },
    },

    methods: {
        fetchContest: async function() {},
        ...mapActions('contests', ['fetchContest']),
    },

    computed: {
        ...mapState('contests', ['contest', 'errors']),
        contestID: function() {
            return this.$route.params.id;
        },
        tabs: function() {
            const result = [
                {
                    name: 'Info',
                    to: {
                        name: 'contest_info',
                        params: { id: this.contestID },
                    },
                },
                {
                    name: 'Tasks',
                    to: {
                        name: 'contest_tasks',
                        params: { id: this.contestID },
                    },
                },
            ];
            if (this.contest && this.contest.can_view_scoreboard) {
                result.push({
                    name: 'Scoreboard',
                    to: {
                        name: 'contest_scoreboard',
                        params: { id: this.contestID },
                    },
                });
            }
            return result;
        },
        scoring: function() {
            return this.contest.dynamic_scoring ? 'dynamic' : 'static';
        },
        timeUntilStart: function() {
            return moment(this.contest.start_time) - moment();
        },
        timeUntilEnd: function() {
            return moment(this.contest.end_time) - moment();
        },

        virtualDuration: function() {
            const regex = /(?:(?<days>\d*) )?(?<hours>\d+):(?<minutes>\d+):(?<seconds>\d+)/;
            const match = this.contest.virtual_duration.match(regex);
            const { days, hours, minutes, seconds } = match.groups;

            let totalSeconds = 0;
            totalSeconds += parseInt(seconds, 10);
            totalSeconds += parseInt(minutes, 10) * 60;
            totalSeconds += parseInt(hours, 10) * 3600;
            if (days) {
                totalSeconds += parseInt(days) * 86400;
            }

            return totalSeconds;
        },
        timeUntilVirtualEnd: function() {
            const opened_at = moment(this.contest.opened_at);
            const virtualEnd = opened_at
                .clone()
                .add(this.virtualDuration, 'seconds');
            const end = moment.min(moment(this.contest.end_time), virtualEnd);
            return end - moment();
        },

        contestState: function() {
            const c = this.contest;
            if (c.is_virtual) {
                if (
                    this.contest.is_running &&
                    Boolean(this.contest.opened_at) &&
                    this.timeUntilVirtualEnd > 0
                ) {
                    return {
                        status: 'RUNNING',
                        time: this.timeUntilVirtualEnd,
                    };
                } else if (
                    this.contest.is_finished ||
                    (Boolean(this.contest.opened_at) &&
                        this.timeUntilVirtualEnd <= 0)
                ) {
                    return { status: 'FINISHED' };
                } else {
                    return { status: 'UPCOMING', time: this.timeUntilStart };
                }
            } else {
                if (c.is_running) {
                    return { status: 'RUNNING', time: this.timeUntilStart };
                } else if (c.is_finished) {
                    return { status: 'FINISHED' };
                } else {
                    return { status: 'UPCOMING', time: this.timeUntilStart };
                }
            }
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

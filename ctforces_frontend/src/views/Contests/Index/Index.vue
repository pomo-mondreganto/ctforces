<template>
    <master-layout>
        <tabs
            :tabs="[
                {
                    name: 'Tasks',
                    to: {
                        name: 'contest_tasks',
                        params: { id: $route.params.id },
                    },
                },
                {
                    name: 'Scoreboard',
                    to: {
                        name: 'contest_scoreboard',
                        params: { id: $route.params.id },
                    },
                },
            ]"
        >
            <router-view />
        </tabs>
        <template v-slot:sidebar v-if="!$types.isNull(contest)">
            <card>
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
                            <template v-slot="props"
                                >Time Remaining：{{ $time(props) }}</template
                            >
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
                            :time="new Date(contest.start_time) - new Date()"
                        >
                            <template v-slot="props"
                                >Starts in {{ $time(props) }}</template
                            >
                        </countdown>
                    </div>
                </div>
            </card>
        </template>
    </master-layout>
</template>

<script>
import Tabs from '@/components/Tabs/Index';

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
};
</script>

<style lang="scss" scoped>
.upcoming {
    color: $reddanger;
}

.running {
    color: $greenlight;
}

.header {
    font-size: 2em;
}
</style>

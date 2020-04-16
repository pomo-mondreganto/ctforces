<template>
    <master-layout>
        <card>
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
        </card>
        <template v-slot:sidebar v-if="!$types.isNull(contest)">
            <card>
                <h1 class="header">
                    {{ contest.name }}
                </h1>
                <div class="author mt-1 mb-2">
                    By
                    <user
                        :username="contest.author_username"
                        :rating="contest.author_rating"
                    />
                </div>
                <div>
                    <countdown :time="2 * 24 * 60 * 60 * 1000">
                        <template v-slot="props"
                            >Time Remaining：{{ time(props) }}</template
                        >
                    </countdown>
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

        time: function(props) {
            let ret = '';
            if (props.days > 1) {
                ret += `${props.days} days `;
            } else if (props.days === 1) {
                ret += `${props.days} day `;
            }
            ret += `${props.hours.toString().padStart(2, '0')}:`;
            ret += `${props.minutes.toString().padStart(2, '0')}:`;
            ret += `${props.seconds.toString().padStart(2, '0')}`;
            return ret;
        },
    },
};
</script>

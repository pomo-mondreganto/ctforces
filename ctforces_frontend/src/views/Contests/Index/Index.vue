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
                    <countdown :time="new Date(contest.end_time) - new Date()">
                        <template v-slot="props"
                            >Time Remaining：{{ time(props) }}</template
                        >
                    </countdown>
                </div>
                <button
                    v-if="contest.is_registration_open"
                    type="button"
                    class="btn mt-1"
                    @click="register"
                >
                    Register
                </button>
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

        register: async function() {
            const { id } = this.$route.params;
            await this.$http.get(`/contests/${id}/register/`);
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

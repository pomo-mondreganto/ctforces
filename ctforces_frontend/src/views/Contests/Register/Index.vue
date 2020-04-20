<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(contest)">
                <f-header :text="`${contest.name} registration`" />
                <form
                    class="mt-2"
                    @submit.prevent="registerForContest"
                    v-if="!$types.isNull(teams)"
                >
                    <div class="ff">
                        <div class="participants">
                            <div class="team-list">
                                <card
                                    :class="[
                                        'team',
                                        teamV.id === team.id ? 'chosen' : '',
                                    ]"
                                    v-for="teamV of teams"
                                    :key="teamV.id"
                                    @click="changeTeam"
                                >
                                    {{ teamV.name }}
                                </card>
                            </div>
                            <card class="participant-list">
                                123
                            </card>
                        </div>
                    </div>
                    <div class="ff">
                        <input type="submit" value="Register" class="btn" />
                    </div>
                </form>
                <f-detail :errors="rerrors['detail']" />
                <pagination :count="count" :pagesize="pagesize" />
            </div>
            <f-detail :errors="cerrors['detail']" />
        </card>
    </master-layout>
</template>

<script>
import FHeader from '@/components/Form/Header';
import Pagination from '@/components/Pagination/Index';
import { mapState } from 'vuex';

export default {
    components: {
        FHeader,
        Pagination,
    },

    data: function() {
        return {
            contest: null,
            teams: null,
            team: { id: null, name: null },
            cerrors: {},
            rerrors: {},
            count: null,
            pagesize: 50,
        };
    },

    created: async function() {
        await this.fetchContest();
        await this.fetchTeams();
    },

    watch: {
        async $route() {
            await this.fetchContest();
            await this.fetchTeams();
        },
    },

    methods: {
        fetchContest: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/contests/${id}/`);
                this.contest = r.data;
            } catch (error) {
                this.cerrors = this.$parse(error.response.data);
            }
        },

        fetchTeams: async function() {
            const { page = 1 } = this.$route.query;
            const { username = null } = this.user;
            if (!this.$types.isNull(username)) {
                try {
                    const r = await this.$http.get(
                        `/users/${username}/teams/?page=${page}`
                    );
                    this.teams = r.data.results;
                    if (this.teams.length > 0) {
                        this.changeTeam(this.teams[0]);
                    } else {
                        this.rerrors['detail'] = ['Register at least one team'];
                    }
                    this.count = r.data.count;
                } catch (error) {
                    this.rerrors = this.$parse(error.response.data);
                }
            }
        },

        registerForContest: async function() {
            try {
                await this.$http.post(`/contest_participant_relationship/`, {
                    contest: this.contest.id,
                    participant: this.user.id,
                });
            } catch (error) {
                this.rerrors = this.$parse(error.response.data);
            }
        },

        changeTeam: function(team) {
            this.team = team;
        },
    },

    computed: mapState(['user']),
};
</script>

<style lang="scss" scoped>
.participants {
    display: flex;
    flex-flow: row nowrap;
}

.team-list {
    flex: 1 1 0;
    margin-right: 1em;
    cursor: pointer;

    & > .team:hover,
    & > .chosen {
        background-color: $gray;
    }
}

.participant-list {
    flex: 1 1 0;
    text-align: center;
}
</style>

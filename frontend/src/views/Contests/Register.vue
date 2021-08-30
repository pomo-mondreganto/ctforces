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
                        <div v-if="teams.length === 0" class="ta-c">
                            <router-link :to="{ name: 'team_create' }"
                                >Create team</router-link
                            >
                        </div>
                        <div class="participants">
                            <div class="team-list">
                                <card
                                    :class="[
                                        'team',
                                        teamV.id === team.id ? 'chosen' : '',
                                    ]"
                                    v-for="teamV of teams"
                                    :key="teamV.id"
                                    @click.native="changeTeam(teamV)"
                                >
                                    {{ teamV.name }}
                                </card>
                            </div>
                            <div class="participant-list">
                                <div v-if="!$types.isNull(users)">
                                    <card
                                        :class="[
                                            'participant',
                                            participants[user.id]
                                                ? 'chosen'
                                                : '',
                                        ]"
                                        v-for="user of users"
                                        :key="user.id"
                                        @click.native="
                                            changeParticipant(user.id)
                                        "
                                    >
                                        {{ user.username }}
                                    </card>
                                </div>
                            </div>
                        </div>
                    </div>
                    <f-detail :errors="rerrors['detail']" />
                    <pagination :count="count" :pagesize="pagesize" />
                    <div class="ff">
                        <input type="submit" value="Register" class="btn" />
                    </div>
                </form>
            </div>
            <f-detail :errors="cerrors['detail']" />
        </card>
    </master-layout>
</template>

<script>
import FHeader from '@/components/Form/Header';
import Pagination from '@/components/Pagination';
import { mapActions, mapState } from 'vuex';

export default {
    components: {
        FHeader,
        Pagination,
    },

    data: function() {
        return {
            teams: null,
            team: { id: null, name: null },
            rerrors: {},
            users: null,
            participants: {},
            count: null,
            pagesize: 50,
        };
    },

    created: async function() {
        await this.fetchContest(this.contestID);
        await this.fetchTeams();
        console.log(this.cerrors);
    },

    watch: {
        async $route() {
            await this.fetchContest(this.contestID);
            await this.fetchTeams();
        },
    },

    methods: {
        ...mapActions('contests', ['fetchContest']),

        fetchTeams: async function() {
            const { page = 1 } = this.$route.query;
            const { username = null } = this.user;
            if (!this.$types.isNull(username)) {
                try {
                    const r = await this.$http.get(
                        `/users/${username}/teams/?page=${page}&page_size=${this.pagesize}`
                    );
                    this.teams = r.data.results;
                    if (this.teams.length > 0) {
                        this.changeTeam(this.teams[0]);
                    }
                    this.count = r.data.count;
                } catch (error) {
                    this.rerrors = this.$parse(error.response.data);
                }
            }
        },

        registerForContest: async function() {
            let toRegister = [];
            for (let user of this.users) {
                if (this.participants[user.id]) {
                    toRegister.push(user.id);
                }
            }
            try {
                await this.$http.post(`/contest_participant_relationship/`, {
                    contest: this.contest.id,
                    participant: this.team.id,
                    registered_users: toRegister,
                });

                this.$toasted.success('Success!');

                if (
                    this.contest.is_running &&
                    toRegister.includes(this.user.id)
                ) {
                    this.$router
                        .push({
                            name: 'contest_info',
                            params: { id: this.contest.id },
                        })
                        .catch(() => {});
                } else {
                    this.$router.push({ name: 'contest_list' }).catch(() => {});
                }
            } catch (error) {
                this.rerrors = this.$parse(error.response.data);
            }
        },

        changeTeam: async function(team) {
            this.team = team;
            this.participants = {};
            try {
                const r = await this.$http.get(`/teams/${team.id}/`);
                this.users = r.data.participants_details;
            } catch (error) {
                this.rerrors = this.$parse(error.response.data);
            }
        },

        changeParticipant: function(id) {
            if (this.participants[id]) {
                this.$set(this.participants, id, false);
            } else {
                this.$set(this.participants, id, true);
            }
        },
    },

    computed: {
        ...mapState(['user']),
        ...mapState('contests', { contest: 'contest', cerrors: 'errors' }),
        contestID: function() {
            return this.$route.params.id;
        },
    },
};
</script>

<style lang="scss" scoped>
.participants {
    display: flex;
    flex-flow: row nowrap;
    align-items: flex-start;
}

.team-list {
    flex: 1 1 0;
    margin-right: 1em;
}

.team {
    cursor: pointer;

    &:hover,
    &.chosen {
        @include use-theme {
            background-color: $gray;
        }
    }
}

.team:not(:last-child) {
    margin-bottom: 1em;
}

.participant-list {
    flex: 1 1 0;
    text-align: center;
}

.participant:not(:last-child) {
    margin-bottom: 1em;
}

.participant {
    cursor: pointer;

    &:hover,
    &.chosen {
        @include use-theme {
            background-color: $gray;
        }
    }
}
</style>

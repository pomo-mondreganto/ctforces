<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(team)" class="p-r">
                <div class="a-tr">
                    <router-link
                        class="team-join btn nlnk"
                        :to="{
                            name: 'team_join',
                            params: { id: $route.params.id },
                        }"
                        v-if="!inTeam"
                    >
                        Join team
                    </router-link>
                </div>
                <f-header class="ta-l" :text="`Team ${team.name}`" />
                <div class="mt-1">Created at {{ createdAt }}</div>
                <div class="mt-1">
                    Captain:
                    <user
                        :rating="team.captain_details.rating"
                        :username="team.captain_details.username"
                    />
                </div>
                <div class="mt-1" v-if="!$types.isNull(token)">
                    Join token: <span class="token">{{ token }}</span>
                </div>
                <f-table
                    class="mt-3"
                    :fields="[
                        {
                            name: '#',
                            pos: 'c',
                            grow: 1,
                        },
                        {
                            name: 'Name',
                            pos: 'l',
                            grow: 11,
                            comp: UserComp,
                        },
                        {
                            name: 'Rating',
                            pos: 'c',
                            key: 'rating',
                            grow: 3,
                        },
                    ]"
                    :data="team.participants_details"
                />
            </div>
            <f-detail :errors="errors['detail']" />
        </card>
    </master-layout>
</template>

<script>
import User from '@/components/Table/User';
import FTable from '@/components/Table/Index';
import FHeader from '@/components/Form/Header';
import { mapState } from 'vuex';
import moment from 'moment';

export default {
    components: {
        FTable,
        FHeader,
    },

    data: function() {
        return {
            errors: {},
            team: null,
            token: null,
            UserComp: User,
        };
    },

    methods: {
        fetchTeam: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/teams/${id}/`);
                this.team = r.data;
                this.team.participants_details = this.team.participants_details.map(
                    (member, index) => {
                        return {
                            '#': index + 1,
                            ...member,
                        };
                    }
                );
                if (this.team.can_edit_team) {
                    try {
                        const r = await this.$http.get(`/teams/${id}/full/`);
                        this.token = r.data.join_token;
                    } catch (error) {
                        this.errors = this.$parse(error.response.data);
                    }
                }
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchTeam();
    },

    watch: {
        $route: async function() {
            await this.fetchTeam();
        },
    },

    computed: {
        ...mapState(['user']),
        inTeam: function() {
            if (this.$types.isNull(this.user)) {
                return false;
            }
            return (
                this.team.participants_details.filter(
                    ({ id }) => id === this.user.id
                ).length > 0
            );
        },
        createdAt: function() {
            return moment(this.team.created_at).format('llll');
        },
    },
};
</script>

<style lang="scss" scoped>
.token {
    @include use-theme {
        color: $bluedark;
    }
}
</style>

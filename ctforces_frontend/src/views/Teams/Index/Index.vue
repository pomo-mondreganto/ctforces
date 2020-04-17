<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(team)">
                <div class="header">Team {{ team.name }}</div>
                <div class="mt-1">
                    Created at {{ new Date(team.created_at) }}
                </div>
                <div class="mt-1">
                    Captain:
                    <user
                        :rating="team.captain_details.rating"
                        :username="team.captain_details.username"
                    />
                </div>
                <f-table
                    v-if="team.participants_details.length > 0"
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

export default {
    components: {
        FTable,
    },

    data: function() {
        return {
            errors: {},
            team: null,
            UserComp: User,
        };
    },

    methods: {
        fetchTeam: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/teams/${id}/full`);
                this.team = r.data;
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
};
</script>

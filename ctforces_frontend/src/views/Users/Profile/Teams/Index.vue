<template>
    <div class="p-r">
        <div
            class="a-tr"
            v-if="
                !$types.isNull(user) && user.username === $route.params.username
            "
        >
            <router-link :to="{ name: 'team_create' }" class="btn nlnk">
                Create team
            </router-link>
        </div>
        <f-header :text="`${$route.params.username} teams`" />
        <div class="mt-1" v-if="!$types.isNull(teams) && teams.length > 0">
            <f-table
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
                        comp: TeamComp,
                    },
                ]"
                :data="teams"
            />
        </div>
        <f-detail :errors="errors['detail']" />
        <pagination :count="count" :pagesize="pagesize" />
    </div>
</template>

<script>
import FHeader from '@/components/Form/Header';
import Team from '@/components/Table/Team';
import { mapState } from 'vuex';
import Pagination from '@/components/Pagination/Index';
import FTable from '@/components/Table/Index';

export default {
    components: {
        FHeader,
        Pagination,
        FTable,
    },

    data: function() {
        return {
            teams: null,
            TeamComp: Team,
            errors: {},
            count: null,
            pagesize: 50,
        };
    },

    methods: {
        fetchTeams: async function() {
            const { page = 1 } = this.$route.query;
            try {
                const r = await this.$http.get(
                    `/users/${this.$route.params.username}/teams/?page=${page}&page_size=${this.pagesize}`
                );
                this.teams = r.data.results.map((team, index) => {
                    return {
                        '#': 1 + index + (page - 1) * this.pagesize,
                        ...team,
                    };
                });
                this.count = r.data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchTeams();
    },

    watch: {
        async $route() {
            await this.fetchTeams();
        },
    },

    computed: mapState(['user']),
};
</script>

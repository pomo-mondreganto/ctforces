<template>
    <full-layout>
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
            <scoreboard
                :data="data"
                :page="$route.query.page"
                :pagesize="pagesize"
            />
            <f-detail :errors="errors['detail']" />
            <pagination :count="count" :pagesize="pagesize" />
        </tabs>
    </full-layout>
</template>

<script>
import Scoreboard from '@/components/Contests/Scoreboard';
import Tabs from '@/components/Tabs';
import Pagination from '@/components/Pagination';

export default {
    components: {
        Scoreboard,
        Tabs,
        Pagination,
    },

    data: function() {
        return {
            data: null,
            errors: {},

            count: null,
            pagesize: 30,
        };
    },

    watch: {
        async $route() {
            await this.fetchScoreboard();
        },
    },

    methods: {
        fetchScoreboard: async function() {
            const { page = 1 } = this.$route.query;
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(
                    `/contests/${id}/scoreboard/?page=${page}&page_size=${this.pagesize}`
                );
                this.data = r.data;
                this.count = r.data.participants.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchScoreboard();
    },
};
</script>

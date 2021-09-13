<template>
    <full-layout>
        <tabs
            :tabs="[
                {
                    name: 'Info',
                    to: {
                        name: 'contest_info',
                        params: { id: contestID },
                    },
                },
                {
                    name: 'Tasks',
                    to: {
                        name: 'contest_tasks',
                        params: { id: contestID },
                    },
                },
                {
                    name: 'Scoreboard',
                    to: {
                        name: 'contest_scoreboard',
                        params: { id: contestID },
                    },
                },
            ]"
        >
            <scoreboard :data="data" :page="currentPage" :pagesize="pagesize" />
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
            const params = { page: this.currentPage, page_size: this.pagesize };
            try {
                const {
                    data,
                } = await this.$http.get(
                    `/contests/${this.contestID}/scoreboard/`,
                    { params }
                );
                this.data = data;
                this.count = data.participants.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchScoreboard();
    },

    computed: {
        contestID: function() {
            return this.$route.params.id;
        },
        currentPage: function() {
            return this.$route.query.page;
        },
    },
};
</script>

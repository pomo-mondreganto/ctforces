<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(task)">
                <f-header :text="`${task.name} solves`" />
                <div class="mt-1" v-if="!$types.isNull(users)">
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
                                comp: UserComp,
                            },
                            {
                                name: 'Rating',
                                pos: 'c',
                                key: 'rating',
                                grow: 3,
                            },
                        ]"
                        :data="users"
                    />
                </div>
                <f-detail :errors="errors['detail']" />
                <pagination :count="count" :pagesize="pagesize" />
            </div>
        </card>
    </master-layout>
</template>

<script>
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import User from '@/components/Table/User';
import Pagination from '@/components/Pagination/Index';

export default {
    components: {
        FHeader,
        FTable,
        Pagination,
    },

    data: function() {
        return {
            task: null,
            users: null,
            UserComp: User,
            errors: {},
            count: null,
            pagesize: 50,
        };
    },

    methods: {
        fetchSolved: async function() {
            const { page = 1 } = this.$route.query;
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(
                    `/tasks/${id}/solved/?page=${page}&page_size=${this.pagesize}`
                );
                this.users = r.data.results.map((user, index) => {
                    return {
                        '#': index + (page - 1) * this.pagesize,
                        ...user,
                    };
                });
                this.count = r.data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        fetchTask: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/tasks/${id}/`);
                this.task = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchTask();
        await this.fetchSolved();
    },

    watch: {
        async $route() {
            await this.fetchTask();
            await this.fetchSolved();
        },
    },
};
</script>

<template>
    <master-layout>
        <card>
            <f-header text="Rating" v-if="!$types.isNull(users)" />
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
            users: null,
            UserComp: User,
            errors: {},
            count: null,
            pagesize: 50,
        };
    },

    methods: {
        fetchRating: async function() {
            const { page = 1 } = this.$route.query;
            try {
                const r = await this.$http.get(
                    `/users/rating_top/?page=${page}`
                );
                this.users = r.data.results.map((user, index) => {
                    return {
                        '#': index,
                        ...user,
                    };
                });
                this.count = r.data.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchRating();
    },

    watch: {
        async $route() {
            await this.fetchRating();
        },
    },
};
</script>

<template>
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
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import FDetail from '@/components/Form/Detail';
import User from '@/components/Table/User';

export default {
    components: {
        Card,
        FHeader,
        FTable,
        FDetail,
    },
    data: function() {
        return {
            users: null,
            UserComp: User,
            errors: {},
        };
    },
    created: async function() {
        const { page = 1 } = this.$route;
        try {
            const r = await this.$http.get(`/users/rating_top/?page=${page}`);
            this.users = r.data.results.map((user, index) => {
                return {
                    '#': index,
                    ...user,
                };
            });
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

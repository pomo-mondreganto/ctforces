<template>
    <card>
        <f-header text="Upsolving" v-if="!isNull(users)" />
        <div class="mt-1" v-if="!isNull(users)">
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

import { isNull } from '@/utils/types';
import parse from '@/utils/errorParser';

export default {
    components: {
        Card,
        FHeader,
        FTable,
        FDetail,
    },
    methods: {
        isNull,
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
            const r = await this.$http.get(
                `/users/upsolving_top/?page=${page}`
            );
            this.users = r.data.results.map((user, index) => {
                return {
                    '#': index,
                    ...user,
                };
            });
        } catch (error) {
            this.errors = parse(error.response.data);
        }
    },
};
</script>

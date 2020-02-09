<template>
    <card>
        <f-header text="Rating" />
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
                        key: 'udata',
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
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import User from '@/components/User/Index';

import { isNull } from '@/utils/types';

export default {
    components: {
        Card,
        FHeader,
        FTable,
    },
    methods: {
        isNull,
    },
    data: function() {
        return {
            users: null,
            UserComp: User,
        };
    },
    created: async function() {
        const { page = 1 } = this.$route;
        try {
            const resp = await this.$http.get(
                `/users/rating_top/?page=${page}`
            );
            this.users = resp.data.results.map((user, index) => {
                return {
                    '#': index,
                    udata: { username: user.username, rating: user.rating },
                    rating: user.rating,
                };
            });
            console.log(this.users);
        } catch {
            console.error('TODO: api is down');
        }
    },
};
</script>

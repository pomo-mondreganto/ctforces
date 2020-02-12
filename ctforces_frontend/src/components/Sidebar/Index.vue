<template>
    <div class="sidebar">
        <card v-if="!$types.isNull(user)" class="mb-2">
            <div class="sidebar-header">{{ user.username }}</div>
            <div class="hr mt-1" />
            <div class="sidebar-profile mt-1">
                <div class="sidebar-profile-left">
                    <div>
                        Rating:
                        <span :class="getInfo(user.rating).class">{{
                            user.rating
                        }}</span>
                    </div>
                    <div class="mt-1">
                        Points:
                        <span :class="getInfo(user.rating).class">{{
                            user.cost_sum
                        }}</span>
                    </div>
                </div>
                <div class="sidebar-profile-right">
                    <img :src="`${serverUrl}${user.avatar_small}`" />
                </div>
            </div>
        </card>
        <card>
            <h2 class="sidebar-header ta-c">Top users</h2>
            <f-table
                class="mt-1"
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
            <f-detail :errors="errors['detail']" />
        </card>
    </div>
</template>

<script>
import { serverUrl } from '@/config';
import Card from '@/components/Card/Index';
import FDetail from '@/components/Form/Detail';
import User from '@/components/Table/User';
import FTable from '@/components/Table/Index';
import { mapState } from 'vuex';
import getInfo from '@/utils/rating';

export default {
    components: {
        Card,
        FDetail,
        FTable,
    },

    data: function() {
        return {
            errors: {},
            users: [],
            UserComp: User,
            serverUrl,
        };
    },

    created: async function() {
        try {
            const r = await this.$http.get('/users/rating_top/?page_size=10');
            this.users = r.data.results.map((user, index) => {
                return { '#': index, ...user };
            });
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },

    computed: mapState(['user']),

    methods: {
        getInfo,
    },
};
</script>

<style lang="scss" scoped>
.sidebar {
    flex: 1 1 0;
}

.sidebar-profile {
    display: flex;

    flex-flow: row nowrap;
    justify-content: space-between;
}
</style>

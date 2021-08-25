<template>
    <div class="sidebar">
        <slot name="top" />
        <card v-if="!$types.isNull(user)" class="mb-2">
            <div class="sidebar-header ta-c">{{ user.username }}</div>
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
                <div class="sidebar-profile-right vc">
                    <img class="sidebar-logo" :src="user.avatar_small" />
                </div>
            </div>
        </card>
        <card>
            <h2 class="sidebar-header ta-c">Top users</h2>
            <f-table
                v-if="!$types.isNull(users)"
                class="mt-1"
                :fields="[
                    {
                        name: '#',
                        pos: 'c',
                        grow: 1,
                        nowrap: true,
                    },
                    {
                        name: 'Name',
                        pos: 'l',
                        grow: 7,
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
        <slot name="bot" />
    </div>
</template>

<script>
import User from '@/components/Table/User';
import FTable from '@/components/Table/Index';
import { mapState } from 'vuex';
import getInfo from '@/utils/rating';

export default {
    components: {
        FTable,
    },

    data: function() {
        return {
            errors: {},
            users: null,
            UserComp: User,
        };
    },

    created: async function() {
        try {
            const r = await this.$http.get(
                '/users/?ordering=-rating,last_solve&page_size=10'
            );
            this.users = r.data.results.map((user, index) => {
                return { '#': index + 1, ...user };
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
.sidebar-profile {
    display: flex;

    flex-flow: row nowrap;
    justify-content: space-between;
}

.sidebar-profile-left {
    flex: 1 0 auto;
}

.sidebar-profile-right {
    min-width: 0;
    flex: 3 1 0;

    .sidebar-logo {
        width: 100%;
    }
}

@media only screen and (max-width: 991px) {
    .sidebar {
        display: none;
    }
}
</style>

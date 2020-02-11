<template>
    <div v-if="!$types.isNull(user)" class="profile">
        <div class="user-info">
            <div :class="getInfo(user.rating).class" class="title">
                {{ getInfo(user.rating).title }}
            </div>
            <user
                :rating="user.rating"
                :username="user.username"
                class="username"
            />
            <div class="rating">
                Rating:
                <span :class="getInfo(user.rating).class">{{
                    user.rating
                }}</span>
            </div>
            <div class="max-rating">
                Maximum rating:
                <span :class="getInfo(user.rating).class">{{
                    user.max_rating
                }}</span>
            </div>
        </div>
        <img class="user-avatar" :src="`${serverUrl}${user.avatar_main}`" />
    </div>
    <f-detail :errors="errors['detail']" v-else />
</template>

<script>
import { serverUrl } from '@/config';
import FDetail from '@/components/Form/Detail';
import getInfo from '@/utils/rating';
import User from '@/components/User/Index';

export default {
    components: {
        FDetail,
        User,
    },
    data: function() {
        return {
            errors: {},
            user: null,
            serverUrl,
        };
    },
    methods: {
        getInfo,
    },
    created: async function() {
        try {
            const r = await this.$http.get(
                `/users/${this.$route.params.username}/`
            );
            this.user = r.data;
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

<style lang="scss" scoped>
.profile {
    display: flex;
    flex-flow: row nowrap;
}

.user-info {
    flex: 1 1 0;
}

.user-avatar {
    flex: 1 1 0;
    max-width: 30%;
}

.title {
    font-size: 1.5em;
}

.username {
    display: block;
    margin-top: 2em;
}

.rating {
    margin-top: 1em;
}

.max-rating {
    margin-top: 1em;
}
</style>

<template>
    <div v-if="!$types.isNull(user)" class="profile">
        <div class="user-info">
            <div :class="getInfo(user.rating).class" class="title">
                {{ getInfo(user.rating).title }}
            </div>
            <user
                :rating="user.rating"
                :username="user.username"
                class="username mt-0-5"
            />
            <div
                v-if="!$types.isUndefined(user.personal_info)"
                class="personal-info mt-1"
            >
                {{ user.personal_info.first_name }}
                {{ user.personal_info.last_name }}
            </div>
            <div
                v-if="!$types.isUndefined(user.personal_info)"
                class="personal-info mt-0-5"
            >
                {{ user.personal_info.telegram }}
            </div>
            <div class="rating mt-1">
                Rating:
                <span :class="getInfo(user.rating).class">{{
                    user.rating
                }}</span>
            </div>
            <div class="max-rating mt-1">
                Maximum rating:
                <span :class="getInfo(user.rating).class">{{
                    user.max_rating
                }}</span>
            </div>
        </div>
        <div class="user-avatar">
            <img class="user-avatar-img" :src="user.avatar_main" />
        </div>
    </div>
    <f-detail :errors="errors['detail']" v-else />
</template>

<script>
import getInfo from '@/utils/rating';

export default {
    data: function() {
        return {
            errors: {},
            user: null,
        };
    },

    methods: {
        getInfo,

        fetchUser: async function() {
            try {
                const r = await this.$http.get(
                    `/users/${this.$route.params.username}/`
                );
                this.user = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchUser();
    },

    watch: {
        async $route() {
            await this.fetchUser();
        },
    },
};
</script>

<style lang="scss" scoped>
.profile {
    display: flex;
    flex-flow: row nowrap;
}

.user-info {
    flex: 2 1 0;
}

.user-avatar {
    flex: 1 1 0;

    .user-avatar-img {
        width: 100%;
    }
}

.username {
    display: inline-block;
    font-size: 1.5em;
}

.personal-info {
    @include use-theme {
        color: $darklight;
    }
}
</style>

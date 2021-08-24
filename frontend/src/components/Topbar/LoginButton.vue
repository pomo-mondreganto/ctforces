<template>
    <router-link
        :to="{ name: 'login' }"
        v-if="$types.isNull(user)"
        class="btn login-button nlnk"
    >
        Login
    </router-link>
    <router-link
        :to="{ name: 'profile', params: { username: user.username } }"
        v-else
        class="btn profile-button nlnk"
    >
        {{ user.username }}
    </router-link>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),
};
</script>

<style lang="scss" scoped>
.login-button {
    @include use-theme {
        color: $white;
        background-color: $green;
        border-color: $green;
    }

    flex: 1 1 0;

    @media only screen and (max-width: 991px) {
        display: none;
    }
}

.profile-button {
    @include use-theme {
        background-color: $bluedark;
        border-color: $bluedark;
    }

    flex: 1 1 0;

    @media only screen and (max-width: 991px) {
        display: none;
    }
}
</style>

<template>
    <button v-if="isNull(user)" @click="loginRedirect" class="btn login-button">
        Login
    </button>
    <button v-else class="btn profile-button" @click="go(user.username)">
        {{ user.username }}
    </button>
</template>

<script>
import { mapState } from 'vuex';
import { isNull } from '@/utils/types';

export default {
    computed: mapState(['user']),
    methods: {
        loginRedirect: function() {
            this.$router.push({ name: 'login' }).catch(() => {});
        },
        go: function(username) {
            this.$router.push({ name: 'profile', params: { username } });
        },
        isNull,
    },
};
</script>

<style lang="scss" scoped>
.login-button {
    color: $white;
    background-color: $green;
    border-color: $green;
    flex: 1 1 0;
}

.profile-button {
    background-color: $bluebtn;
    border-color: $bluebtn;
    flex: 1 1 0;
}
</style>

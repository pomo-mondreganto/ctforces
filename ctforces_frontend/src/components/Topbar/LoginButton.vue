<template>
    <button v-if="user !== null" class="lb">
        {{ user.username }}
    </button>
    <button v-else @click="loginRedirect" class="btn lb">
        Login
    </button>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),
    methods: {
        loginRedirect: function() {
            this.$router.push({ name: 'login' }).catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.lb {
    color: $green;
    border-color: $green;
}
.lb:hover {
    color: $dark;
    border-color: $dark;
}
</style>

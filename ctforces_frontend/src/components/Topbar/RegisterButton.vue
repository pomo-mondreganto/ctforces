<template>
    <button v-if="user !== null" class="lb" @click="logout">
        Logout
    </button>
    <button v-else @click="registerRedirect" class="btn rb">
        Register
    </button>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),
    methods: {
        registerRedirect: function() {
            this.$router.push({ name: 'register' }).catch(() => {});
        },
        logout: async function() {
            await this.$http.post('/logout/');
            await this.$store.dispatch('GET_ME');
        },
    },
};
</script>

<style lang="scss" scoped>
.rb {
    color: $red;
    border-color: $red;
}
.rb:hover {
    color: $dark;
    border-color: $dark;
}
</style>

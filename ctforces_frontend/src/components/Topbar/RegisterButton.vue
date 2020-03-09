<template>
    <button
        type="button"
        v-if="$types.isNull(user)"
        @click="registerRedirect"
        class="btn register-button ml-0-5"
    >
        Register
    </button>
    <button
        type="button"
        v-else
        class="btn logout-button out ml-0-5"
        @click="logout"
    >
        Logout
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
            await this.$store.dispatch('UPDATE_USER');

            if (this.$route.meta.auth) {
                this.$router
                    .push({
                        name: 'login',
                        query: { redirect: this.$route.name },
                    })
                    .catch(() => {});
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.register-button {
    color: $white;
    background-color: $darklight;
    border-color: $darklight;
    flex: 1 1 0;
}

.logout-button {
    background-color: $red;
    border-color: $red;
    flex: 1 1 0;
}
</style>

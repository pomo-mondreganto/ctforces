<template>
    <button
        v-if="isNull(user)"
        @click="registerRedirect"
        class="btn register-button"
    >
        Register
    </button>
    <button v-else class="btn logout-button out" @click="logout">
        Logout
    </button>
</template>

<script>
import { mapState } from 'vuex';
import { isNull } from '@/utils/types';

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
                this.$router.push({
                    name: 'login',
                    query: { redirect: this.$route.name },
                });
            }
        },
        isNull,
    },
};
</script>

<style lang="scss" scoped>
.register-button {
    color: $white;
    background-color: $darklight;
    border-color: $darklight;
    margin-left: 0.5em;
    flex: 1 1 0;
}

.logout-button {
    background-color: $red;
    border-color: $red;
    margin-left: 0.5em;
    flex: 1 1 0;
}
</style>

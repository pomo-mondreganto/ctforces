<template>
    <router-link
        :to="{ name: 'register' }"
        v-if="$types.isNull(user)"
        class="btn register-button ml-0-5 nlnk"
    >
        Register
    </router-link>
    <a
        href="#"
        v-else
        class="nlnk btn logout-button out ml-0-5"
        @click="logout"
    >
        Logout
    </a>
</template>

<script>
import { mapState } from 'vuex';

export default {
    computed: mapState(['user']),

    methods: {
        logout: async function() {
            await this.$http.post('/logout/');
            await this.$store.dispatch('UPDATE_USER');

            this.$router
                .push({
                    name: 'index',
                })
                .catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.register-button {
    @include use-theme {
        color: $white;
        background-color: $darklight;
        border-color: $darklight;
    }
    flex: 1 1 0;

    @media only screen and (max-width: 991px) {
        display: none;
    }
}

.logout-button {
    @include use-theme {
        background-color: $red;
        border-color: $red;
    }
    flex: 1 1 0;

    @media only screen and (max-width: 991px) {
        display: none;
    }
}
</style>

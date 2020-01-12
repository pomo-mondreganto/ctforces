<template>
    <button v-if="isNull(user)" @click="loginRedirect" class="btn lb">
        Login
    </button>
    <button v-else class="btn lb">
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
        isNull,
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

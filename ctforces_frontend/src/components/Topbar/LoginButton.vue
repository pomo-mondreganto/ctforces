<template>
    <button v-if="isNull(user)" @click="loginRedirect" class="btn lb log">
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
    color: $white;
    background-color: $green;
    border-color: $green;
}

.lb.log {
    background-color: $bluebtn;
    border-color: $bluebtn;
}
</style>

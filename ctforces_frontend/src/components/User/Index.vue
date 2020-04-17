<template>
    <a :class="getInfo(rating).class" class="user" @click="go(username)">{{
        username
    }}</a>
</template>

<script>
import getInfo from '@/utils/rating';

export default {
    props: {
        username: String,
        rating: Number,
    },

    methods: {
        getInfo,

        go: function() {
            this.$router
                .push({
                    name: 'profile',
                    params: { username: this.username },
                })
                .catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.user {
    cursor: pointer;
}
</style>

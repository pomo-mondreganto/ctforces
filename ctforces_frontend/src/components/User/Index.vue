<template>
    <router-link
        :to="{
            name: 'profile',
            params: { username: this.username },
        }"
        :class="getInfo(rating).class"
        class="user nlnk"
        >{{ username }}</router-link
    >
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
    },
};
</script>

<style lang="scss" scoped>
.user {
    cursor: pointer;
}
</style>

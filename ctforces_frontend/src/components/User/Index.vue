<template>
    <span :class="getClass(rating)" @click="go(username)">{{ username }}</span>
</template>

<script>
export default {
    props: {
        username: String,
        rating: Number,
    },
    methods: {
        getClass: function() {
            return ['red', 'user'];
        },
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

.red {
    color: $red;
}
</style>

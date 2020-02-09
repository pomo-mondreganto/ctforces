<template>
    <span :class="getClass(rating)">{{ username }}</span>
</template>

<script>
export default {
    props: {
        username: String,
        rating: Number,
    },
    methods: {
        getClass: function() {
            console.log(this.rating);
            console.log(this.username);
            return 'red';
        },
    },
};
</script>

<style lang="scss" scoped>
.red {
    color: $red;
}
</style>

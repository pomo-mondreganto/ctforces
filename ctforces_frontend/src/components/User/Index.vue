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

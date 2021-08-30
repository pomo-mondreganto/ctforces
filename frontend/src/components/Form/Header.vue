<template>
    <h1 class="header ta-c">{{ text }}</h1>
</template>

<script>
export default {
    props: {
        text: String,
    },
};
</script>

<style lang="scss" scoped>
.header {
    font-size: 1.6em;

    @include use-theme {
        color: $black;
    }
}
</style>

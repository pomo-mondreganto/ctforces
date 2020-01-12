<template>
    <h1 class="header tac">
        {{ text }}
    </h1>
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
    font-size: 2em;
    color: $black;
}
</style>

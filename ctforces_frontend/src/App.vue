<template>
    <router-view />
</template>

<script>
export default {
    mounted: async function() {
        await this.$store.dispatch('UPDATE_USER');
    },
};
</script>

<style lang="scss">
@import './styles/reset.css';
@import './styles/main.scss';
</style>

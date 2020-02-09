<template>
    <master>
        <router-view />
    </master>
</template>

<script>
import Master from '@/layouts/Master';

export default {
    created: async function() {
        await this.$store.dispatch('UPDATE_USER');
    },
    components: {
        Master,
    },
};
</script>

<style lang="scss">
@import './styles/main.scss';
@import '~simplemde/dist/simplemde.min.css';
</style>

<template>
    <router-view />
</template>

<script>
export default {
    created: async function() {
        const theme = localStorage.getItem('theme');
        if (!this.$types.isNull(theme)) {
            document.body.classList.add('dark-theme');
        }

        await this.$store.dispatch('UPDATE_USER');
    },
};
</script>

<style lang="scss">
@import './styles/main.scss';
@import '~simplemde/dist/simplemde.min.css';
@import '~vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
</style>

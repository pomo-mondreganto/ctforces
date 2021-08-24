<template>
    <div class="hamburger" @click="toggleSidebar">☰</div>
</template>

<script>
export default {
    methods: {
        toggleSidebar: function() {
            this.$store.dispatch('TOGGLE_SIDEBAR');
        },
    },
};
</script>

<style lang="scss" scoped>
.hamburger {
    flex: 1 1 0;
    font-size: 3em;
    cursor: pointer;
    text-align: right;
    padding-right: 0.7em;

    @media only screen and (min-width: 992px) {
        display: none;
    }
}
</style>

<template>
    <span @click="go" :class="['menu-nav', 'ta-c', active ? 'active' : '']">{{
        text
    }}</span>
</template>

<script>
export default {
    props: {
        to: String,
        text: String,
    },

    methods: {
        go: function() {
            this.$router.push({ name: this.to }).catch(() => {});
        },
    },

    computed: {
        active: function() {
            return this.$route.name == this.to;
        },
    },
};
</script>

<style lang="scss" scoped>
.menu-nav {
    cursor: pointer;
    width: 15%;
    color: $darklight;
}

.active,
.menu-nav:hover {
    color: $black;
    font-weight: 800;
}
</style>

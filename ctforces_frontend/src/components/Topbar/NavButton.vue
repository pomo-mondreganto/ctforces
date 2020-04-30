<template>
    <router-link
        :to="{ name: to }"
        :class="['menu-nav', 'ta-c', 'nlnk', active ? 'active' : '']"
    >
        {{ text }}
    </router-link>
</template>

<script>
export default {
    props: {
        to: String,
        text: String,
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
    flex: 1 0 0;
    @include use-theme {
        color: $darklight;
    }
}

.active,
.menu-nav:hover {
    @include use-theme {
        color: $black;
    }
    font-weight: 800;
}
</style>

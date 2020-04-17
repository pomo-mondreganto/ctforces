<template>
    <div class="tabs">
        <div class="tabs-tabs">
            <a
                v-for="tab of tabs"
                :key="tab.name"
                class="tab"
                @click="go(tab.to)"
                :class="$route.name === tab.to.name ? 'active' : ''"
            >
                {{ tab.name }}
            </a>
        </div>
        <div class="tabs-content">
            <slot />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        tabs: Array,
    },
    methods: {
        go: function(to) {
            this.$router.push(to).catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.tabs {
    display: flex;
    flex-flow: column nowrap;
}

.tabs-tabs {
    display: flex;
    flex-flow: row nowrap;
    height: 3em;
}

.tab {
    flex: 1 1 0;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;

    &:not(.active) {
        border-bottom: 1px solid rgba($darklight, 0.2);
    }

    &.active,
    &:hover {
        border-top-left-radius: 0.4em;
        border-top-right-radius: 0.4em;
        border-top: 1px solid rgba($darklight, 0.2);
        border-left: 1px solid rgba($darklight, 0.2);
        border-right: 1px solid rgba($darklight, 0.2);
    }
}

.tabs-content {
    border-left: 1px solid rgba($darklight, 0.2);
    border-right: 1px solid rgba($darklight, 0.2);
    border-bottom: 1px solid rgba($darklight, 0.2);
    padding: 1em;
    border-bottom-left-radius: 0.4em;
    border-bottom-right-radius: 0.4em;
    min-height: 5em;
}
</style>

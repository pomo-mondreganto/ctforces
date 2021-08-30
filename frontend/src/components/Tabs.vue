<template>
    <div class="tabs pr-1 pl-1">
        <div class="tabs-tabs">
            <router-link
                :to="tab.to"
                class="tab nlnk link td-n"
                v-for="tab of tabs"
                :key="tab.name"
                :class="$route.name === tab.to.name ? 'active' : ''"
            >
                {{ tab.name }}
            </router-link>
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
        @include use-theme {
            border-bottom: 1px solid rgba($darklight, 0.2);
        }
    }

    &.active,
    &:hover {
        border-top-left-radius: 0.4em;
        border-top-right-radius: 0.4em;
        @include use-theme {
            border-top: 1px solid rgba($darklight, 0.2);
            border-left: 1px solid rgba($darklight, 0.2);
            border-right: 1px solid rgba($darklight, 0.2);
        }
    }
}

.tabs-content {
    @include use-theme {
        border-left: 1px solid rgba($darklight, 0.2);
        border-right: 1px solid rgba($darklight, 0.2);
        border-bottom: 1px solid rgba($darklight, 0.2);
    }
    padding: 1em;
    border-bottom-left-radius: 0.4em;
    border-bottom-right-radius: 0.4em;
    min-height: 3em;
}
</style>

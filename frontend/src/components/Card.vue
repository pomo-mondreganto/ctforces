<template>
    <div class="inside p-1">
        <slot />
    </div>
</template>

<style lang="scss" scoped>
.inside {
    @include use-theme {
        border: 0.05em solid rgba($darklight, 0.5);
    }
    border-radius: 0.4em;
    min-height: 3em;
}
</style>

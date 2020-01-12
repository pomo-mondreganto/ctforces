<template>
    <div>
        <div class="inside">
            <slot />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.inside {
    border: 0.05em solid rgba($darklight, 0.5);
    border-radius: 0.4em;
    padding: 1em;
}
</style>

<template>
    <div class="inside p-1">
        <slot />
    </div>
</template>

<style lang="scss" scoped>
.inside {
    border: 0.05em solid rgba($darklight, 0.5);
    border-radius: 0.4em;
}
</style>

<style lang="scss">
.inside .p-r .a-tr {
    padding-right: 1em;
}
</style>

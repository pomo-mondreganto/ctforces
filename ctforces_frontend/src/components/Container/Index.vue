<template>
    <div class="container">
        <slot />
    </div>
</template>

<style lang="scss" scoped>
.container {
    margin-left: 7em;
    margin-right: 7em;

    @media only screen and (max-width: 991px) {
        margin-left: 0;
        margin-right: 0;
    }
}
</style>

<template>
    <span class="tag wb-a ta-c">
        <slot />
    </span>
</template>

<style lang="scss" scoped>
.tag {
    border: 0.05em solid $graytags;
    color: $graytags;
    border-radius: 0.2em;
    font-size: 0.9em;
    padding: 0.3em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
    margin: 0.15em;

    &:hover {
        background-color: $graytags;
        color: $white;
        cursor: pointer;
    }
}
</style>

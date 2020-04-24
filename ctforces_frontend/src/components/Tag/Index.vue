<template>
    <router-link
        :to="{ name: 'task_list', query: { tag: name } }"
        class="nlnk tag wb-a ta-c"
    >
        {{ name }}
    </router-link>
</template>

<script>
export default {
    props: {
        name: String,
    },
};
</script>

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

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
    @include use-theme {
        border: 0.05em solid $graytags;
        color: $graytags;
    }
    border-radius: 0.2em;
    font-size: 0.9em;
    padding: 0.3em;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
    margin: 0.15em;

    &:hover {
        @include use-theme {
            background-color: $graytags;
            color: $white;
        }
        cursor: pointer;
    }
}
</style>

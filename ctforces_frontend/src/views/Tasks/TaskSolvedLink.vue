<template>
    <router-link :to="url">{{ field }}</router-link>
</template>

<script>
export default {
    props: {
        field: Number,
        row: Object,
    },
    computed: {
        url: function() {
            return `/tasks/${this.row.id}/solved`;
        },
    },
};
</script>

<template>
    <router-link :to="url">{{ row[fieldName] }}</router-link>
</template>

<script>
export default {
    props: {
        fieldName: String,
        row: Object,
    },
    computed: {
        url: function() {
            return `/tasks/${this.row.id}`;
        },
    },
};
</script>

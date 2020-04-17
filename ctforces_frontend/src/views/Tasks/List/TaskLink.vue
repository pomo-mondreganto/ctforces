<template>
    <a @click="go" class="link">{{ row[fieldName] }}</a>
</template>

<script>
export default {
    props: {
        fieldName: String,
        row: Object,
    },

    methods: {
        go: function() {
            this.$router
                .push({ name: 'task_index', params: { id: this.row.id } })
                .catch(() => {});
        },
    },
};
</script>

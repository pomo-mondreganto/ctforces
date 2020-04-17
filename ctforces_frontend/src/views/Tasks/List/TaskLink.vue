<template>
    <router-link
        :to="{ name: 'task_index', params: { id: row.id } }"
        class="link"
        >{{ row[fieldData] }}</router-link
    >
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

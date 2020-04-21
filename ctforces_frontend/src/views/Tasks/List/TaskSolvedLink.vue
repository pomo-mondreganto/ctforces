<template>
    <router-link
        class="link"
        :to="{ name: 'task_solved', params: { id: row.id } }"
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

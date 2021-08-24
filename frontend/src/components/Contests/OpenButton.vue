<template>
    <router-link
        class="link nlnk"
        :to="{ name: 'contest_tasks', params: { id: row.id } }"
    >
        Open
    </router-link>
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

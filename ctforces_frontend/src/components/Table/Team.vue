<template>
    <router-link
        :to="{ name: 'team_index', params: { id: row['id'] } }"
        class="nlnk link"
        >{{ row['name'] }}</router-link
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

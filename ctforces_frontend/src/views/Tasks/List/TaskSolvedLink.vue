<template>
    <router-link class="link" :to="{ name: 'index' }">{{
        row[fieldData]
    }}</router-link>
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

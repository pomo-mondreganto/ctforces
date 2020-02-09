<template>
    <span>{{ row[fieldName] }}</span>
</template>

<script>
export default {
    props: {
        fieldName: [String, Number],
        row: Object,
    },
};
</script>

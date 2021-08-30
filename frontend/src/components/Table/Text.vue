<template>
    <span>{{ row[fieldData] }}</span>
</template>

<script>
export default {
    props: {
        fieldData: [String, Number],
        row: Object,
    },
};
</script>

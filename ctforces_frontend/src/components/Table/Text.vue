<template>
    <span>{{ field }}</span>
</template>

<script>
export default {
    props: {
        field: [String, Number],
        row: Object,
    },
};
</script>

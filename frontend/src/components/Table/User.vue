<template>
    <user :username="row.username" :rating="row.rating" />
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

<template>
    <user :username="row['username']" :rating="row['rating']" />
</template>

<script>
export default {
    props: {
        fieldName: String,
        row: Object,
    },
};
</script>

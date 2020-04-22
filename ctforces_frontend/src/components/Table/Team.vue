<template>
    <team :id="row.id" :name="row.name" :rating="row.rating" />
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

<template>
    <countdown :time="new Date(row[fieldData]) - new Date()">
        <template v-slot="props">{{ $time(props) }}</template>
    </countdown>
</template>

<script>
export default {
    props: {
        fieldData: String,
        row: Object,
    },
};
</script>

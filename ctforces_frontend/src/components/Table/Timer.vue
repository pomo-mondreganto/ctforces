<template>
    <countdown :time="new Date(row[fieldData]) - new Date()">
        <template v-slot="props">
            <span class="countdown">{{ $time(props.time) }}</span>
        </template>
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

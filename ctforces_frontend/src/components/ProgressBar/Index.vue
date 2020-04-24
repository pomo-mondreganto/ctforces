<template>
    <div class="ff" v-if="!$types.isNull(value)">
        <v-progress-bar :value="value * 100" bar-class="pb-success" />
    </div>
</template>

<script>
export default {
    props: {
        value: Number,
    },
};
</script>

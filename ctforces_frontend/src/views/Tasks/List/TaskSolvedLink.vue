<template>
    <div class="link" @click="go()">{{ row[fieldName] }}</div>
</template>

<script>
export default {
    props: {
        fieldName: String,
        row: Object,
    },
    methods: {
        go: function() {
            this.$router.push({ name: 'index' }).catch(() => {});
        },
    },
};
</script>

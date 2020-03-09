<template>
    <a class="link" @click="go">{{ row[fieldName] }}</a>
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

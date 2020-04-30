<template>
    <div class="group" v-if="invalid">
        <div v-for="error of errors" :key="error" class="error">
            {{ error }}
        </div>
    </div>
</template>

<script>
export default {
    props: {
        errors: Array,
    },
    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },
    },
};
</script>

<style lang="scss" scoped>
.group {
    width: 100%;
}

.error {
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
    width: 100%;
}
</style>

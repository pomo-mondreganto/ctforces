<template>
    <div class="group">
        <v-select
            :options="options"
            :value="value"
            @input="val => $emit('input', val)"
        />
        <div v-if="invalid">
            <div v-for="error of errors" :key="error" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        value: String,
        options: Array,
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
.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

<template>
    <div class="group">
        <input
            v-bind="$attrs"
            :value="value"
            @change="$emit('fileChanged', $event.target.files)"
            class="input file"
            type="file"
            :invalid="invalid"
        />
        <label class="label">{{ label }}</label>
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
        label: String,
        value: String,
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
$height-input: 2.6em;
$height-label: 1em;
$border: 0.05em;

.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

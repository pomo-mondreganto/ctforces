<template>
    <div class="group">
        <input
            v-bind="$attrs"
            @input="$emit('input', $event.target.checked)"
            class="input"
            type="checkbox"
            :checked="value"
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
        value: Boolean,
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
$height-input: 1.5em;
$height-label: 0.9em;
$border: 0.05em;
$inv-height-label: math.div(1em, $height-label);

.group {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    padding-left: 0.2em;
}

.input {
    padding: 0;
    outline: none;
    font-family: inherit;
    font-size: $height-label;
    height: $height-input * $inv-height-label;
    @include use-theme {
        border: $border * $inv-height-label solid $darklight;
    }
    border-radius: $inv-height-label * 0.3em;

    &[invalid] {
        @include use-theme {
            border-color: $reddanger;
        }
    }
}

.input[type='checkbox'] {
    display: flex;
}

.label {
    display: flex;
    padding-left: 0.5em;
}

.error {
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

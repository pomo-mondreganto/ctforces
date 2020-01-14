<template>
    <div class="group">
        <input
            v-bind="$attrs"
            :value="value"
            @input="$emit('input', $event.target.value)"
            :class="['input', !value ? '' : 'non-empty']"
            :invalid="invalid"
        />
        <label class="label">{{ placeholder }}</label>
        <div v-if="invalid">
            <div v-for="error in errors" :key="error" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
import { isArray } from '@/utils/types';

export default {
    props: {
        placeholder: String,
        value: String,
        errors: Array,
    },
    methods: {
        isArray,
    },
    computed: {
        invalid: function() {
            return isArray(this.errors) && this.errors.length > 0;
        },
    },
};
</script>

<style lang="scss" scoped>
$height-input: 2.2em;
$height-label: 1.2em;
$border: 0.05em;

.group {
    position: relative;
}

.input {
    padding: 0;
    outline: none;
    font-family: inherit;
    font-size: $height-label;
    height: $height-input * (1em / $height-label);
    padding-left: 0.4em;
    border: $border * (1em / $height-label) solid $darklight;
    border-radius: (1em / $height-label) * 0.3em;

    &:focus {
        border-color: $bluelight;
    }

    &[invalid] {
        border-color: $reddanger;
    }

    &:focus + .label,
    &.non-empty + .label {
        font-size: 85%;
        top: -1em;
        left: 0;
        color: rgba($black, 1);
    }

    width: calc(100% - 0.4em - #{$border * (1em / $height-label)});
}

.label {
    position: absolute;
    font-size: $height-label;
    top: (1em / $height-label) * ($height-input + 2 * $border) / 2 - 0.5em;
    left: 0.4em;
    transition: all 200ms;
    color: rgba($black, 0.5);
    pointer-events: none;
}

.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

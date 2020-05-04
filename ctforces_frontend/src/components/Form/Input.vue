<template>
    <div class="group">
        <input
            v-bind="$attrs"
            :value="value"
            @input="$emit('input', $event.target.value)"
            :class="['input', !value ? '' : 'non-empty'].concat(outerClasses)"
            :invalid="invalid"
        />
        <label class="label">{{ placeholder }}</label>
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
        placeholder: String,
        value: String,
        errors: Array,
        customClasses: Array,
    },

    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },

        outerClasses: function() {
            if (this.$types.isUndefined(this.customClasses)) {
                return [];
            }
            return this.customClasses;
        },
    },
};
</script>

<style lang="scss" scoped>
$height-input: 2.6em;
$height-label: 1em;
$border: 0.05em;

.group {
    position: relative;
}

.input:disabled {
    @include use-theme {
        background-color: $gray;
    }
}

.input {
    @include use-theme {
        color: $black;
        background-color: $white;
    }
    padding: 0;
    outline: none;
    font-family: inherit;
    font-size: $height-label;
    height: $height-input * (1em / $height-label);
    padding-left: 0.4em;
    @include use-theme {
        border: $border * (1em / $height-label) solid $darklight;
    }
    border-radius: (1em / $height-label) * 0.3em;

    &:focus {
        @include use-theme {
            border-color: $bluelight;
        }
    }

    &[invalid] {
        @include use-theme {
            border-color: $reddanger;
        }
    }

    &:focus + .label,
    &.non-empty + .label {
        font-size: 85%;
        top: -1.2em;
        left: 0;
        @include use-theme {
            color: rgba($black, 1);
        }
    }

    width: calc(100% - 0.4em - #{$border * (1em / $height-label)});
}

.label {
    position: absolute;
    font-size: $height-label;
    padding-left: 0.3em;
    top: (1em / $height-label) * ($height-input + 2 * $border) / 2 - 0.5em;
    left: 0.4em;
    transition: all 200ms;
    @include use-theme {
        color: rgba($black, 0.5);
    }
    pointer-events: none;
}

.error {
    @include use-theme {
        color: $red;
    }
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

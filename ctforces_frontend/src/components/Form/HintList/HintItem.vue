<template>
    <div class="mb-1">
        <f-input
            type="text"
            name="body"
            :value="value.body"
            @input="changeBody"
            placeholder="Body"
            class="mr-1"
        />
        <f-checkbox
            name="is_published"
            :value="value.is_published"
            @input="changePub"
            label="Published"
        />
    </div>
</template>

<script>
import FInput from '@/components/Form/Input';
import FCheckbox from '@/components/Form/Checkbox';

export default {
    props: {
        value: Object,
        index: Number,
    },

    methods: {
        changeBody: function(body) {
            this.$emit('input', { ...this.value, body });
        },

        changePub: function(is_published) {
            this.$emit('input', { ...this.value, is_published });
        },
    },

    components: {
        FInput,
        FCheckbox,
    },
};
</script>

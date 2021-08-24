<template>
    <div class="mb-1">
        <f-input
            :value="value.body"
            class="mr-1"
            name="body"
            placeholder="Body"
            type="text"
            @input="changeBody"
        />
        <f-checkbox
            :value="value.is_published"
            label="Published"
            name="is_published"
            @input="changePub"
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

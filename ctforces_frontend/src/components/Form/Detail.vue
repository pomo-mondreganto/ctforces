<template>
    <div class="group" v-if="invalid">
        <div v-for="error in errors" :key="error" class="error">
            {{ error }}
        </div>
    </div>
</template>

<script>
import { isArray } from '@/utils/types';

export default {
    props: {
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
.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

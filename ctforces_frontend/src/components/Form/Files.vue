<template>
    <div class="group">
        <input
            v-bind="$attrs"
            @change="changeFiles($event.target.files)"
            class="input file"
            type="file"
            :invalid="invalid"
            ref="finput"
            multiple
        />
        <label class="label">{{ label }}</label>
        <div
            class="file-list mt-1"
            v-for="(file, index) of value"
            :key="file.id"
        >
            <div class="btn file-list-remove-btn" @click="removeFile(index)">
                Remove
            </div>
            <div class="file-list-name pl-0-5">
                {{ file.name }}
            </div>
        </div>
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
        value: Array,
        errors: Array,
    },

    computed: {
        invalid: function() {
            return this.$types.isArray(this.errors) && this.errors.length > 0;
        },
    },

    methods: {
        changeFiles: function(files) {
            let filesArr = this.value;
            for (let file of files) {
                file.id = this._.uniqueId('file');
                filesArr.push(file);
            }
            this.$emit('input', filesArr);
            this.$refs.finput.value = '';
        },

        removeFile: function(index) {
            this.$emit(
                'input',
                this.value.filter((el, i) => i !== index)
            );
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

.file-list {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.file-list-remove-btn {
    display: flex;
    flex-grow: 0 0 1em;
}

.file-list-name {
    display: flex;
    flex: 0 0 100em;
}

.error {
    color: $red;
    margin-top: 0.3em;
    font-size: 0.8em;
}
</style>

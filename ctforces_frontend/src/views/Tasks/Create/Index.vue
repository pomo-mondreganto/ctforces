<template>
    <card>
        <f-header header text="Create task"></f-header>
        <form class="def-form mt-2" @submit.prevent="createTask">
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="name"
                    v-model="name"
                    :errors="errors['name']"
                    placeholder="Name"
                ></f-input>
            </div>
            <div class="ff">
                <vue-tags-input
                    v-model="tag"
                    :tags="tags"
                    :autocomplete-items="autocompleteTags"
                    :max-tags="5"
                    :maxlength="15"
                    @tags-changed="newTags => (tags = newTags)"
                />
                <div v-if="tagsInvalid">
                    <div
                        v-for="error of errors['tags']"
                        :key="error"
                        class="error"
                    >
                        {{ error }}
                    </div>
                </div>
            </div>
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="cost"
                    v-model="cost"
                    :errors="errors['cost']"
                    placeholder="Cost"
                ></f-input>
            </div>
            <div class="ff">
                <f-input
                    class="mt-1-5"
                    type="text"
                    name="flag"
                    v-model="flag"
                    :errors="errors['flag']"
                    placeholder="Flag"
                ></f-input>
            </div>
            <div class="ff">
                <editor v-model="description" :errors="errors['description']" />
            </div>
            <div class="ff mt-0">
                <f-checkbox
                    name="is_published"
                    v-model="is_published"
                    label="Published"
                    :errors="errors['is_published']"
                ></f-checkbox>
            </div>
            <div class="ff mt-1">
                <f-file-field
                    name="file"
                    label="Upload files"
                    @fileChanged="fileChanged"
                    :errors="errors['files']"
                ></f-file-field>
            </div>
            <div
                class="file-list mt-1"
                v-for="(file, index) in attachedFiles"
                v-bind:key="index"
            >
                <div
                    class="btn file-list-remove-btn"
                    @click="removeFile(index)"
                >
                    Remove
                </div>
                <div class="file-list-name pl-0-5">
                    {{ file.name }}
                </div>
            </div>
            <div class="ff">
                <input type="submit" value="Create" class="btn" />
            </div>
        </form>
    </card>
</template>

<style lang="scss" scoped>
.vue-tags-input {
    max-width: 100%;
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

<script>
import VueTagsInput from '@johmun/vue-tags-input';
import Editor from '@/components/Editor/Index';
import Card from '@/components/Card/Index';
import FHeader from '@/components/Form/Header';
import FInput from '@/components/Form/Input';
import FCheckbox from '@/components/Form/Checkbox';
import FFileField from '@/components/Form/FileField';

export default {
    components: {
        Card,
        FHeader,
        FInput,
        Editor,
        FCheckbox,
        FFileField,
        VueTagsInput,
    },
    data: function() {
        return {
            name: null,
            description: null,
            cost: null,
            flag: null,
            is_published: false,
            attachedFiles: [],
            errors: {},
            tag: '',
            tags: [],
            autocompleteTags: [],
        };
    },
    methods: {
        tagsChanged(newTags) {
            this.tags = newTags;
        },
        createFiles: async function() {
            let fileIds = [];
            for await (const file of this.attachedFiles) {
                let form = new FormData();
                form.set('name', file.name);
                form.append('file_field', file);
                try {
                    const resp = await this.$http({
                        url: '/task_files/',
                        method: 'post',
                        data: form,
                        headers: { 'Content-Type': 'multipart/form-data' },
                    });
                    fileIds.push(resp.data.id);
                } catch (error) {
                    this.$set(
                        this.errors,
                        'files',
                        error.response.data['file_field']
                    );
                }
            }
            return fileIds;
        },
        createTags: async function() {
            let tagIds = [];
            let toCreate = [];
            for await (const tag of this.tags) {
                const tagName = tag.text;
                const resp = await this.$http.get(
                    `/task_tags/search/?name=${tagName}`
                );

                if (resp.data.length > 0 && resp.data[0].name == tagName) {
                    tagIds.push(resp.data[0].id);
                    continue;
                }

                toCreate.push({ name: tagName });
            }
            try {
                const resp = await this.$http.post(`/task_tags/`, toCreate);
                resp.data.forEach(tag => tagIds.push(tag.id));
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }

            return tagIds;
        },
        createTask: async function() {
            if (this.attachedFiles.length > 5) {
                this.errors['files'] = '5 files at most';
                return;
            }
            const fileIds = await this.createFiles();
            const tagIds = await this.createTags();
            try {
                const resp = await this.$http.post('/tasks/', {
                    name: this.name,
                    cost: this.cost,
                    flag: this.flag,
                    description: this.description,
                    is_published: this.is_published,
                    files: fileIds,
                    tags: tagIds,
                    hints: [],
                });
                this.$router
                    .push({
                        name: 'task_index',
                        params: { id: resp.data.id },
                    })
                    .catch(() => {});
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
        fileChanged: async function(files) {
            if (files.length == 0) {
                return;
            }
            this.attachedFiles.push(files[0]);
        },
        removeFile: async function(index) {
            this.attachedFiles.splice(index, 1);
        },
    },
    computed: {
        tagsInvalid: function() {
            return (
                this.$types.isArray(this.errors['tags']) &&
                this.errors['tags'].length > 0
            );
        },
    },
    watch: {
        tag: async function(currentTag) {
            if (currentTag.length == 0) {
                return;
            }
            try {
                const resp = await this.$http.get(
                    `/task_tags/search/?name=${currentTag}`
                );
                this.autocompleteTags = resp.data.map(value => {
                    return { text: value.name };
                });
            } catch (error) {
                this.autocompleteTags = [];
            }
        },
    },
};
</script>

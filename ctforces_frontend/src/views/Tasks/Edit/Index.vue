<template>
    <master-layout>
        <card>
            <f-header header text="Update task"></f-header>
            <form class="mt-2" @submit.prevent="updateTask">
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="name"
                        v-model="name"
                        :errors="errors['name']"
                        placeholder="Name"
                    />
                </div>
                <div class="ff">
                    <f-tags
                        class="mt-1-5"
                        v-model="tags"
                        :errors="errors['tags']"
                        name="tags"
                    />
                </div>
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="cost"
                        v-model="cost"
                        :errors="errors['cost']"
                        placeholder="Cost"
                    />
                </div>
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="flag"
                        v-model="flag"
                        :errors="errors['flag']"
                        placeholder="Flag"
                    />
                </div>
                <div class="ff">
                    <editor
                        v-model="description"
                        :errors="errors['description']"
                    />
                </div>
                <div class="ff mt-0">
                    <f-checkbox
                        name="is_published"
                        v-model="is_published"
                        label="Published"
                        :errors="errors['is_published']"
                    />
                </div>
                <div class="ff mt-1">
                    <f-files
                        name="file"
                        label="Upload files"
                        v-model="attachedFiles"
                        :errors="errors['files']"
                    />
                </div>
                <div class="ff">
                    <input type="submit" value="Update" class="btn" />
                </div>
            </form>
        </card>
    </master-layout>
</template>

<script>
import Editor from '@/components/Editor/Index';
import FHeader from '@/components/Form/Header';
import FInput from '@/components/Form/Input';
import FCheckbox from '@/components/Form/Checkbox';
import FFiles from '@/components/Form/Files';
import FTags from '@/components/Form/Tags';

export default {
    components: {
        FHeader,
        FInput,
        Editor,
        FCheckbox,
        FFiles,
        FTags,
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
            tags: [],
            autocompleteTags: [],
        };
    },

    created: async function() {
        try {
            const resp = await this.$http.get(
                `/tasks/${this.$route.params.id}/full/`
            );
            this.name = resp.data.name;
            this.description = resp.data.description;
            this.cost = String(resp.data.cost);
            this.flag = resp.data.flag;
            this.isPublished = resp.data.is_published;
            this.attachedFiles = resp.data.files_details;
            this.tags = resp.data.task_tags_details.map(tag => {
                return { text: tag.name };
            });
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },

    methods: {
        createFiles: async function() {
            let fileIds = [];
            for await (const file of this.attachedFiles) {
                if (file.id !== undefined) {
                    fileIds.push(file.id);
                    continue;
                }
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
                    return { ok: false };
                }
            }
            return { ok: true, ids: fileIds };
        },

        createTags: async function() {
            let tagIds = [];
            let toCreate = [];
            for await (const tag of this.tags) {
                const tagName = tag.text;
                const resp = await this.$http.get(
                    `/task_tags/search?name=${tagName}/`
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
                return { ok: false };
            }

            return { ok: true, ids: tagIds };
        },

        updateTask: async function() {
            if (this.attachedFiles.length > 5) {
                this.errors['files'] = '5 files at most';
                return;
            }
            const { ok: ok1, ids: fileIds } = await this.createFiles();
            if (!ok1) {
                return;
            }
            const { ok: ok2, ids: tagIds } = await this.createTags();
            if (!ok2) {
                return;
            }
            try {
                const resp = await this.$http.put(
                    `/tasks/${this.$route.params.id}/`,
                    {
                        name: this.name,
                        cost: this.cost,
                        flag: this.flag,
                        description: this.description,
                        is_published: this.isPublished,
                        files: fileIds,
                        tags: tagIds,
                        hints: [],
                    }
                );
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
    },
};
</script>

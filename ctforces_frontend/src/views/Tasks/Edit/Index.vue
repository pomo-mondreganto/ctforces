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
                <hint-list v-model="hints" />
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
                <progress-bar :value="progress" />
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Update" class="btn" />
                </div>
            </form>
        </card>
    </master-layout>
</template>

<script>
    import HintList from '@/components/Form/HintList/Index';
    import Editor from '@/components/Editor/Index';
    import FHeader from '@/components/Form/Header';
    import FInput from '@/components/Form/Input';
    import FCheckbox from '@/components/Form/Checkbox';
    import FFiles from '@/components/Form/Files';
    import FTags from '@/components/Form/Tags';
    import ProgressBar from '@/components/ProgressBar/Index';

    export default {
        components: {
            FHeader,
            FInput,
            Editor,
            FCheckbox,
            FFiles,
            FTags,
            ProgressBar,
            HintList,
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
            hints: [],
            oldHints: {},
            autocompleteTags: [],
            progress: null,
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
            this.hints = resp.data.hints_details.map(
                ({ id, body, task, is_published }) => {
                    this.oldHints[id] = true;
                    return {
                        hid: id,
                        id: task,
                        body,
                        is_published,
                    };
                }
            );
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
            for (const file of this.attachedFiles) {
                let form = new FormData();
                form.set('name', file.name);
                form.append('file_field', file);
                try {
                    let self = this;
                    const resp = await this.$http.post('/task_files/', form, {
                        onUploadProgress: function(progressEvent) {
                            self.progress =
                                progressEvent.loaded / progressEvent.total;
                        },
                    });
                    fileIds.push(resp.data.id);
                } catch (error) {
                    this.errors = this.$parse(error.response.data);
                    return null;
                }
            }
            this.progress = null;
            return fileIds;
        },

        createTags: async function() {
            let tagIds = [];
            let toCreate = [];
            for (const tag of this.tags) {
                const tagName = tag.text;
                const resp = await this.$http.get(`/task_tags?name=${tagName}`);

                if (
                    resp.data.results.length > 0 &&
                    resp.data.results[0].name == tagName
                ) {
                    tagIds.push(resp.data.results[0].id);
                    continue;
                }

                toCreate.push({ name: tagName });
            }
            try {
                const resp = await this.$http.post(`/task_tags/`, toCreate);
                resp.data.forEach(tag => tagIds.push(tag.id));
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                return null;
            }

            return tagIds;
        },

        createHints: async function(taskId) {
            try {
                let newHints = {};

                for (const hint of this.hints) {
                    if (hint.hid) {
                        newHints[hint.hid] = true;
                    }
                    if (hint.hid && this.oldHints[hint.hid]) {
                        await this.$http.put(`/task_hints/${hint.hid}/`, {
                            task: taskId,
                            body: hint.body,
                            is_published: hint.is_published,
                        });
                    } else {
                        await this.$http.post('/task_hints/', {
                            task: taskId,
                            body: hint.body,
                            is_published: hint.is_published,
                        });
                    }
                }

                for (const hint_id in this.oldHints) {
                    if (!newHints[hint_id]) {
                        await this.$http.delete(`/task_hints/${hint_id}/`);
                    }
                }
            } catch (error) {
                this.errors = this.$parse(error.response.data);
                return null;
            }
            return true;
        },

        updateTask: async function() {
            const fileIds = await this.createFiles();
            if (this.$types.isNull(fileIds)) {
                return;
            }
            const tagIds = await this.createTags();
            if (this.$types.isNull(tagIds)) {
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
                await this.createHints(resp.data.id);
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

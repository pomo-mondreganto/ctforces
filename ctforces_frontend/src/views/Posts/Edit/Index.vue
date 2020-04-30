<template>
    <master-layout>
        <card>
            <f-header header text="Edit post"></f-header>
            <form class="mt-2" @submit.prevent="editPost">
                <div class="ff">
                    <f-input
                        class="mt-1-5"
                        type="text"
                        name="title"
                        v-model="title"
                        :errors="errors['title']"
                        placeholder="Title"
                    />
                </div>
                <div class="ff">
                    <editor v-model="body" :errors="errors['body']" />
                </div>
                <div class="ff mt-0">
                    <f-checkbox
                        name="is_published"
                        v-model="is_published"
                        label="Published"
                        :errors="errors['is_published']"
                    />
                </div>

                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Edit" class="btn" />
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

export default {
    components: {
        FHeader,
        FInput,
        Editor,
        FCheckbox,
    },

    data: function() {
        return {
            title: null,
            body: null,
            is_published: false,
            errors: {},
        };
    },

    created: async function() {
        try {
            const r = await this.$http.get(`/posts/${this.$route.params.id}/`);
            this.title = r.data.title;
            this.body = r.data.body;
            this.is_published = r.data.is_published;
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },

    methods: {
        editPost: async function() {
            try {
                const resp = await this.$http.put(
                    `/posts/${this.$route.params.id}/`,
                    {
                        title: this.title,
                        body: this.body,
                        is_published: this.is_published,
                    }
                );
                this.$router
                    .push({
                        name: 'post_index',
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

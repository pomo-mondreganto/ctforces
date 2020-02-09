<template>
    <card>
        <div v-if="!isNull(task)">
            <h1 class="header">
                {{ task.name }}
            </h1>
            <div class="author mt-1">
                By
                <user
                    :username="task.author_username"
                    :rating="task.author_rating"
                />
            </div>
            <div class="tags mt-1">
                <span class="tags-h">Tags:</span>
                <tag v-for="tag in task.tags_details" :key="tag.id">{{
                    tag.name
                }}</tag>
            </div>
            <div class="hr"></div>
            <div class="content mt-1">
                <div class="markdown">
                    <markdown :content="task.description"></markdown>
                </div>
            </div>
            <div class="hr mt-1"></div>
            <div class="files mt-1" v-if="task.files_details.length > 0">
                <div>Files:</div>
                <a
                    :href="mediaUrl + file.file_field"
                    target="_blank"
                    v-for="file in task.files_details"
                    :key="file.id"
                >
                    {{ file.name }}
                </a>
            </div>
            <div class="hr mt-1" v-if="task.files_details.length > 0"></div>
            <form class="def-form mt-2" @submit.prevent="submit">
                <f-input
                    type="text"
                    name="flag"
                    v-model="flag"
                    :errors="errors['flag']"
                    placeholder="Flag"
                />
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Submit" class="btn" />
                </div>
            </form>
        </div>
        <f-detail :errors="errors['detail']" />
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
import { isNull, isUndefined } from '@/utils/types';
import User from '@/components/User/Index';
import Tag from '@/components/Tag/Index';
import { mediaUrl } from '@/config';
import Markdown from '@/components/Markdown/Index';
import FInput from '@/components/Form/Input';
import FDetail from '@/components/Form/Detail';
import parse from '@/utils/errorParser';

export default {
    components: {
        Card,
        User,
        Tag,
        Markdown,
        FInput,
        FDetail,
    },
    created: async function() {
        const { id } = this.$route.params;
        try {
            const r = await this.$http.get(`/tasks/${id}`);
            this.task = r.data;
        } catch (error) {
            this.errors = parse(error.response.data);
        }
    },
    data: function() {
        return {
            task: null,
            mediaUrl: mediaUrl,
            flag: null,
            errors: {},
        };
    },
    methods: {
        isNull,
        submit: async function() {
            const { id } = this.$route.params;
            try {
                await this.$http.post(`/tasks/${id}/submit/`, {
                    flag: this.flag,
                });
                this.$toasted.success('Valid flag!');
            } catch (error) {
                this.errors = parse(error.response.data);
                if (
                    !isUndefined(this.errors['flag']) &&
                    this.errors['flag'].length > 0 &&
                    this.errors['flag'][0] === 'Invalid flag.'
                ) {
                    this.$toasted.error('Invalid flag!');
                }
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.header {
    font-size: 2em;
    margin-top: 0.5em;
}

.tags {
    margin-bottom: 1em;
    display: flex;
    flex-flow: row wrap;
    align-items: center;

    .tags-h {
        margin-right: 0.5em;
    }
}

.hr {
    border-bottom: 1px solid $gray;
}

.content {
    border-left: 0.3em solid $gray;
}

.markdown {
    margin-left: 1em;
}
</style>

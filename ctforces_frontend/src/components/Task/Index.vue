<template>
    <div v-if="!$types.isNull(task)">
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
        <div class="tags mt-1 mb-1">
            <span class="tags-h">Tags:</span>
            <tag v-for="tag of task.tags_details" :key="tag.id">{{
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
                :href="`${mediaUrl}/${file.file_field}`"
                target="_blank"
                v-for="file of task.files_details"
                :key="file.id"
            >
                {{ file.name }}
            </a>
        </div>
        <div class="hr mt-1" v-if="task.files_details.length > 0"></div>
        <form class="mt-2" @submit.prevent="submitFlag">
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
</template>

<script>
import Tag from '@/components/Tag/Index';
import { mediaUrl } from '@/config';
import Markdown from '@/components/Markdown/Index';
import FInput from '@/components/Form/Input';

export default {
    props: {
        task: Object,
        errors: Object,
        submitFlag: Function,
    },

    components: {
        Tag,
        Markdown,
        FInput,
    },

    data: function() {
        return {
            mediaUrl,
            flag: null,
        };
    },
};
</script>

<style lang="scss" scoped>
.tags {
    display: flex;
    flex-flow: row wrap;
    align-items: center;

    .tags-h {
        margin-right: 0.5em;
    }
}

.content {
    border-left: 0.3em solid $gray;
}

.markdown {
    margin-left: 1em;
    padding: 1em;
}
</style>

<template>
    <div v-if="!$types.isNull(post)">
        <router-link
            :to="{ name: 'post_index', params: { id: post.id } }"
            class="header link"
        >
            {{ post.title }}
        </router-link>
        <div class="mt-1">
            By
            <user
                :username="post.author_username"
                :rating="post.author_rating"
            />, {{ new Date(post.created_at) }}
        </div>
        <div class="hr mt-1" />
        <div class="content mt-1">
            <div class="markdown ml-1 p-1">
                <markdown :content="post.body" />
            </div>
        </div>
    </div>
</template>

<script>
import Markdown from '@/components/Markdown/Index';

export default {
    props: {
        post: Object,
    },

    components: {
        Markdown,
    },
};
</script>

<style lang="scss" scoped>
.content {
    border-left: 0.3em solid $gray;
}

.header {
    font-size: 2em;
}
</style>

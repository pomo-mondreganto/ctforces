<template>
    <div v-if="!$types.isNull(post)">
        <h1 class="header link" @click="go">
            {{ post.title }}
        </h1>
        <div class="mt-1">
            By
            <user
                :username="post.author_username"
                :rating="post.author_rating"
            />, {{ new Date(post.created_at) }}
        </div>
        <div class="hr mt-1" />
        <div class="content mt-1">
            <div class="markdown">
                <markdown :content="post.body" />
            </div>
        </div>
    </div>
</template>

<script>
import User from '@/components/User/Index';
import Markdown from '@/components/Markdown/Index';

export default {
    props: {
        post: Object,
    },

    components: {
        User,
        Markdown,
    },

    methods: {
        go: function() {
            this.$router
                .push({ name: 'post_index', params: { id: this.post.id } })
                .catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.markdown {
    margin-left: 1em;
    padding: 1em;
}

.content {
    border-left: 0.3em solid $gray;
}
</style>

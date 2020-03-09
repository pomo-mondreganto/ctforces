<template>
    <div v-if="!$types.isNull(post)">
        <a class="header link" @click="go">
            {{ post.title }}
        </a>
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
.content {
    border-left: 0.3em solid $gray;
}
</style>

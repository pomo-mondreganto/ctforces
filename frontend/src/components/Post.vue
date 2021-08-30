<template>
    <div v-if="!$types.isNull(post)">
        <div v-if="!$types.isNull(post) && post.can_edit_post" class="p-r">
            <div class="a-tr">
                <router-link
                    :to="{ name: 'post_edit', params: { id: post.id } }"
                    class="btn nlnk"
                >
                    Edit post
                </router-link>
            </div>
        </div>
        <router-link
            :to="{ name: 'post_index', params: { id: post.id } }"
            class="header link"
        >
            {{ post.title }}
        </router-link>
        <div class="mt-1-5">
            <span>By </span>
            <user
                :rating="post.author_rating"
                :username="post.author_username"
            />
            {{ createdAt }}
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
import Markdown from '@/components/Markdown';
import moment from 'moment';

export default {
    props: {
        post: Object,
    },

    components: {
        Markdown,
    },

    computed: {
        createdAt: function() {
            return moment(this.post.created_at).format('llll');
        },
    },
};
</script>

<style lang="scss" scoped>
.content {
    @include use-theme {
        border-left: 0.3em solid $gray;
    }
}

.header {
    font-size: 1.5em;
}
</style>

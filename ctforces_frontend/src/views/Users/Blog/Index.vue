<template>
    <div>
        <div
            v-for="(post, index) in posts"
            :key="post.id"
            :class="index > 0 ? 'mt-3' : ''"
        >
            <post :post="post" />
        </div>
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import Post from '@/components/Post/Index';
import FDetail from '@/components/Form/Detail';

export default {
    data: function() {
        return {
            posts: [],
            errors: {},
        };
    },

    components: {
        Post,
        FDetail,
    },

    created: async function() {
        try {
            const r = await this.$http.get(
                `/users/${this.$route.params.username}/posts/`
            );
            this.posts = r.data.results;
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

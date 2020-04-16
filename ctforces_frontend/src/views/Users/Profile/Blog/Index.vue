<template>
    <div class="p-r">
        <div class="a-tr">
            <button type="button" @click="createPost()" class="btn">
                Create post
            </button>
        </div>
        <div
            v-for="(post, index) of posts"
            :key="post.id"
            :class="index > 0 ? 'mt-3' : 'pt-1'"
        >
            <post :post="post" />
        </div>
        <f-detail :errors="errors['detail']" />
        <pagination :count="count" :pagesize="pagesize" />
    </div>
</template>

<script>
import Post from '@/components/Post/Index';
import Pagination from '@/components/Pagination/Index';
import { mapState } from 'vuex';

export default {
    data: function() {
        return {
            posts: [],
            errors: {},
            count: null,
            pagesize: 10,
        };
    },

    components: {
        Post,
        Pagination,
    },

    methods: {
        fetchPosts: async function(page) {
            try {
                const r = await this.$http.get(
                    `/users/${this.$route.params.username}/posts/?page=${page}&page_size=${this.pagesize}`
                );
                this.count = r.data.count;
                this.posts = r.data.results;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        createPost: function() {
            this.$router.push({ name: 'post_create' }).catch(() => {});
        },
    },

    created: async function() {
        const { page = 1 } = this.$route.query;
        await this.fetchPosts(page);
    },

    watch: {
        async $route() {
            const { page = 1 } = this.$route.query;
            await this.fetchPosts(page);
        },
    },

    computed: mapState(['user']),
};
</script>

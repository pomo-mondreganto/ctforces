<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(posts) && posts.length > 0">
                <div
                    v-for="(post, index) of posts"
                    :key="post.id"
                    :class="index > 0 ? 'mt-3' : 'pt-1'"
                >
                    <post :post="post" />
                </div>
            </div>
            <div v-else-if="!$types.isNull(posts) && posts.length === 0">
                No records here
            </div>
            <f-detail :errors="errors['detail']" />
            <pagination :count="count" :pagesize="pagesize" />
        </card>
    </master-layout>
</template>

<script>
import Pagination from '@/components/Pagination/Index';
import Post from '@/components/Post/Index';

export default {
    components: {
        Pagination,
        Post,
    },

    data: function() {
        return {
            posts: null,
            errors: {},
            count: null,
            pagesize: 10,
        };
    },

    methods: {
        fetchPosts: async function(page) {
            try {
                const r = await this.$http.get(
                    `/posts/?page=${page}&page_size=${this.pagesize}`
                );
                this.count = r.data.count;
                this.posts = r.data.results;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        const { page = 1 } = this.$route.query;
        await this.fetchPosts(page);
    },

    watch: {
        $route: async function() {
            const { page = 1 } = this.$route.query;
            await this.fetchPosts(page);
        },
    },
};
</script>

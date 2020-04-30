<template>
    <div class="p-r">
        <div
            class="a-tr"
            v-if="
                !$types.isNull(user) && user.username === $route.params.username
            "
        >
            <router-link :to="{ name: 'post_create' }" class="btn nlnk">
                Create post
            </router-link>
        </div>
        <f-header :text="`${$route.params.username} blog`" />
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
    </div>
</template>

<script>
import FHeader from '@/components/Form/Header';
import Post from '@/components/Post/Index';
import Pagination from '@/components/Pagination/Index';
import { mapState } from 'vuex';

export default {
    data: function() {
        return {
            posts: null,
            errors: {},
            count: null,
            pagesize: 10,
        };
    },

    components: {
        Post,
        Pagination,
        FHeader,
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

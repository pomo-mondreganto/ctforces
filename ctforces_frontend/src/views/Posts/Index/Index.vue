<template>
    <master-layout>
        <card>
            <post :post="post" />
            <f-detail :errors="errors['detail']" />
        </card>
    </master-layout>
</template>

<script>
import Post from '@/components/Post/Index';

export default {
    data: function() {
        return {
            errors: {},
            post: null,
        };
    },

    components: {
        Post,
    },

    methods: {
        fetchPost: async function() {
            try {
                const r = await this.$http.get(
                    `/posts/${this.$route.params.id}/`
                );
                this.post = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchPost();
    },

    watch: {
        async $route() {
            await this.fetchPost();
        },
    },
};
</script>

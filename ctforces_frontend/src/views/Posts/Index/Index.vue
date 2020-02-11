<template>
    <card>
        <post :post="post" />
        <f-detail :errors="errors['detail']" />
    </card>
</template>

<script>
import Card from '@/components/Card/Index';
import FDetail from '@/components/Form/Detail';
import Post from '@/components/Post/Index';

export default {
    data: function() {
        return {
            errors: {},
            post: null,
        };
    },

    components: {
        Card,
        FDetail,
        Post,
    },

    created: async function() {
        try {
            const r = await this.$http.get(`/posts/${this.$route.params.id}/`);
            this.post = r.data;
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

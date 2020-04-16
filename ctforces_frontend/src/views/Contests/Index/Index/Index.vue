<template>
    <div>
        <contest :contest="contest" :errors="errors" />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import Contest from '@/components/Contest/Index';

export default {
    data: function() {
        return {
            contest: null,
            errors: {},
        };
    },

    components: {
        Contest,
    },

    created: async function() {
        await this.fetchContest();
    },

    watch: {
        async $route() {
            await this.fetchContest();
        },
    },

    methods: {
        fetchContest: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/contests/${id}/`);
                this.contest = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

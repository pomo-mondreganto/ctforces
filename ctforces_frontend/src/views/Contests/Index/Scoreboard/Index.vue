<template>
    <div>
        <scoreboard :data="solves" />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import Scoreboard from '@/components/Scoreboard/Index';

export default {
    components: {
        Scoreboard,
    },

    data: function() {
        return {
            solves: null,
            errors: {},
        };
    },

    watch: {
        async $route() {
            await this.fetchScoreboard();
        },
    },

    methods: {
        fetchScoreboard: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/contests/${id}/scoreboard`);
                this.solved = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchScoreboard();
    },
};
</script>

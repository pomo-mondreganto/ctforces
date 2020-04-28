<template>
    <div>
        <div
            class="p-r"
            v-if="!$types.isNull(contest) && contest.can_edit_contest"
        >
            <div class="a-tr">
                <router-link
                    :to="{ name: 'contest_edit', params: { id: contest.id } }"
                    class="btn nlnk"
                >
                    Edit contest
                </router-link>
            </div>
        </div>
        <contest :contest="contest" :contest_tasks="contest_tasks" />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
import Contest from '@/components/Contest/Index';

export default {
    data: function() {
        return {
            contest: null,
            contest_tasks: null,
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
                const rc = await this.$http.get(`/contests/${id}/`);
                this.contest = rc.data;
                const rt = await this.$http.get(`/contests/${id}/tasks/`);
                this.contest_tasks = rt.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

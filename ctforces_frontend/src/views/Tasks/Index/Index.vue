<template>
    <master-layout>
        <card>
            <task :task="task" :errors="serrors" :submitFlag="submit" />
            <f-detail :errors="errors['detail']" />
        </card>
    </master-layout>
</template>

<script>
import Task from '@/components/Task/Index';

export default {
    components: {
        Task,
    },

    created: async function() {
        await this.fetchTask();
    },

    data: function() {
        return {
            task: null,
            errors: {},
            serrors: {},
        };
    },

    watch: {
        async $route() {
            await this.fetchTask();
        },
    },

    methods: {
        fetchTask: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/tasks/${id}/`);
                this.task = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        submit: async function(flag) {
            const { id } = this.$route.params;
            try {
                await this.$http.post(`/tasks/${id}/submit/`, {
                    flag: flag,
                });
                this.$toasted.success('Valid flag!');
            } catch (error) {
                this.serrors = this.$parse(error.response.data);
                if (
                    !this.$types.isUndefined(this.serrors['flag']) &&
                    this.serrors['flag'].length > 0 &&
                    this.serrors['flag'][0] === 'Invalid flag.'
                ) {
                    this.$toasted.error('Invalid flag!');
                }
            }
        },
    },
};
</script>

<template>
    <div>
        <div v-if="Object.keys(errors).length === 0">Redirecting...</div>
        <f-detail :errors="errors['token']" />
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            errors: {},
        };
    },

    created: async function() {
        const { token } = this.$route.query;

        try {
            await this.$http.post('/confirm_email/', {
                token,
            });
            this.$toasted.success('Success!');
            this.$router.push({ name: 'login' }).catch(() => {});
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

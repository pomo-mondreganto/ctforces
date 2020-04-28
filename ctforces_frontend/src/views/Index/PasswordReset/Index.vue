<template>
    <master-layout>
        <card>
            <f-header text="Password reset" />
            <form class="mt-3" @submit.prevent="reset">
                <div class="ff">
                    <f-input
                        type="email"
                        name="email"
                        v-model="email"
                        :errors="errors['email']"
                        placeholder="Email"
                    />
                </div>
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Reset" class="btn" />
                </div>
            </form>
        </card>
    </master-layout>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';

export default {
    components: {
        FInput,
        FHeader,
    },
    data: function() {
        return {
            email: null,
            errors: {},
        };
    },
    methods: {
        reset: async function() {
            try {
                await this.$http.post('/request_password_reset/', {
                    email: this.email,
                });
                this.$toasted.info(
                    'You have asked for password reset. Check your email'
                );
                this.$router.push({ name: 'index' }).catch(() => {});
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

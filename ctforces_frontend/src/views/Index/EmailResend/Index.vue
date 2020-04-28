<template>
    <master-layout>
        <card>
            <f-header text="Resend email" />
            <form class="mt-3" @submit.prevent="resend">
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
                    <input type="submit" value="Resend" class="btn" />
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
        resend: async function() {
            try {
                await this.$http.post('/resend_confirmation/', {
                    email: this.email,
                });
                this.$toasted.info(
                    'You have asked for resending. Check your email'
                );
                this.$router.push({ name: 'index' }).catch(() => {});
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

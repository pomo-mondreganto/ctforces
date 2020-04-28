<template>
    <master-layout>
        <card>
            <f-header text="Password reset confirmation" />
            <form class="mt-3" @submit.prevent="reset">
                <div class="ff">
                    <f-input
                        type="password"
                        name="password"
                        v-model="password"
                        :errors="errors['password']"
                        placeholder="Password"
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
    data: function() {
        return {
            password: null,
            errors: {},
        };
    },

    components: {
        FHeader,
        FInput,
    },

    created: async function() {
        const { token } = this.$route.query;

        try {
            await this.$http.post('/reset_password/', {
                password: this.password,
                token,
            });

            this.$router.push({ name: 'login' }).catch(() => {});
        } catch (error) {
            this.errors = this.$parse(error.response.data);
        }
    },
};
</script>

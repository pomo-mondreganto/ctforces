<template>
    <master-layout>
        <card>
            <f-header text="Register" />
            <form class="mt-3" @submit.prevent="register">
                <div class="ff">
                    <f-input
                        type="text"
                        name="login"
                        v-model="username"
                        :errors="errors['username']"
                        placeholder="Username"
                        required
                    />
                </div>
                <div class="ff">
                    <f-input
                        type="email"
                        name="email"
                        v-model="email"
                        :errors="errors['email']"
                        placeholder="Email"
                        required
                    />
                </div>
                <div class="ff">
                    <f-input
                        type="password"
                        name="password"
                        v-model="password"
                        :errors="errors['password']"
                        placeholder="Password"
                        required
                    />
                </div>
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Register" class="btn" />
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
            username: null,
            email: null,
            password: null,
            errors: {},
        };
    },
    methods: {
        register: async function() {
            try {
                await this.$http.post('/register/', {
                    username: this.username,
                    email: this.email,
                    password: this.password,
                });
                this.$toasted.info(
                    "We've sent a confirmation email. Please check your email"
                );
                this.$router.push({ name: 'login' }).catch(() => {});
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

<template>
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
</template>

<script>
import Card from '@/components/Card/Index';
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FDetail from '@/components/Form/Detail';

export default {
    components: {
        FInput,
        Card,
        FHeader,
        FDetail,
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
                this.$router.push({ name: 'login' }).catch(() => {});
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

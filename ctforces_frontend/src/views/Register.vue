<template>
    <layout>
        <card>
            <f-header text="Register" />
            <form class="def-form" @submit.prevent="register">
                <f-input
                    type="text"
                    name="login"
                    v-model="username"
                    :errors="errors['username']"
                    placeholder="Username"
                    required
                />
                <f-input
                    type="email"
                    name="email"
                    v-model="email"
                    :errors="errors['email']"
                    placeholder="Email"
                    required
                />
                <f-input
                    type="password"
                    name="password"
                    v-model="password"
                    :errors="errors['password']"
                    placeholder="Password"
                    required
                />
                <f-detail :errors="errors['detail']" />
                <input type="submit" value="Register" class="btn" />
            </form>
        </card>
    </layout>
</template>

<script>
import Layout from '@/layouts/Master';
import Card from '@/components/Card/Index';
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FDetail from '@/components/Form/Detail';

import parse from '@/utils/errorParser';

export default {
    components: {
        Layout,
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
                this.$router.push({ name: 'login' });
            } catch (error) {
                this.errors = parse(error.response.data);
            }
        },
    },
};
</script>

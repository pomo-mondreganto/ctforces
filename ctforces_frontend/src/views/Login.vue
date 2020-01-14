<template>
    <layout>
        <card>
            <f-header text="Login" />
            <form class="def-form" @submit.prevent="login">
                <f-input
                    type="text"
                    name="login"
                    v-model="username"
                    :errors="errors['username']"
                    placeholder="Username"
                />
                <f-input
                    type="password"
                    name="password"
                    v-model="password"
                    :errors="errors['password']"
                    placeholder="Password"
                />
                <f-detail :errors="errors['detail']" />
                <input type="submit" value="Login" class="btn" />
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
import { isUndefined } from '@/utils/types';

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
            password: null,
            errors: {},
        };
    },
    methods: {
        login: async function() {
            try {
                await this.$http.post('/login/', {
                    username: this.username,
                    password: this.password,
                });
                await this.$store.dispatch('UPDATE_USER');

                if (!isUndefined(this.$route.query.redirect)) {
                    this.$router.push({ name: this.$route.query.redirect });
                } else {
                    this.$router.push({ name: 'index' });
                }
            } catch (error) {
                this.errors = parse(error.response.data);
            }
        },
    },
};
</script>

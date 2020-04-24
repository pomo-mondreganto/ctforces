<template>
    <master-layout>
        <card>
            <f-header text="Login" />
            <form class="mt-3" @submit.prevent="login">
                <div class="ff">
                    <f-input
                        type="text"
                        name="login"
                        v-model="username"
                        :errors="errors['username']"
                        placeholder="Username"
                    />
                </div>
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
                    <input type="submit" value="Login" class="btn" />
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

                const route = localStorage.getItem('route');

                if (!this.$types.isNull(route)) {
                    localStorage.removeItem('route');
                    this.$router.push(JSON.parse(route)).catch(() => {});
                } else {
                    this.$router.push({ name: 'index' }).catch(() => {});
                }
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

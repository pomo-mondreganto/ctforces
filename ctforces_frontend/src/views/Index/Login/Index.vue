<template>
    <card>
        <f-header text="Login" />
        <form class="def-form mt-3" @submit.prevent="login">
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

                if (!this.$types.isUndefined(this.$route.query.redirect)) {
                    this.$router
                        .push({ name: this.$route.query.redirect })
                        .catch(() => {});
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

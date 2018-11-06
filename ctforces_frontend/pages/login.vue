<template>
    <div class="ui segment">
        <div>Sign In</div>
        <div class="ui clearing divider"></div>
        <form class="ui form error warning" @submit.prevent="login">
            <div class="field">
                <input type="text" name="username" placeholder="Handle" v-model="loginForm.username">
            </div>
            <div class="field">
                <input type="password" name="password" placeholder="Password" v-model="loginForm.password"/>
            </div>
            <div v-if="loginForm.errors['detail']" class="ui error message">
                {{ loginForm.errors['detail'] }}
            </div>
            <button class="ui fluid teal button field" type="submit">Sign me in</button>
            <div class="field center_aligned">
                <div>If you have an account and forget your password, please
                    <nuxt-link to="/">reset it</nuxt-link>.
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    layout: 'base',
    data() {
        return {
            loginForm: {
                username: '',
                password: '',
                errors: {}
            }
        };
    },
    methods: {
        async login() {
            try {
                await this.$store.dispatch('auth/login', {
                    username: this.loginForm.username,
                    password: this.loginForm.password
                });
            } catch (e) {
                let { data } = e.response;
                this.loginForm.errors = data;
            }
        }
    }
};
</script>

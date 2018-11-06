<template>
    <div class="ui centered grid">
        <div class="sixteen wide column">
            <div class="ui basic segment">
                <div>Sign In</div>
                <div class="ui clearing divider"></div>
                <form class="ui basic vertical segment form error warning" @submit.prevent="login">
                    <div class="field" v-bind:class="formErrors['username']">
                        <input type="text" name="username" placeholder="Handle" v-model="formUsername">
                    </div>
                    <div class="field" v-bind:class="formErrors['password']">
                        <input type="password" name="password" placeholder="Password" v-model="formPassword"/>
                    </div>
                    <div v-if="formErrors['detail']" class="ui error message">
                        {{ formErrors['detail'] }}
                    </div>
                    <button class="ui fluid teal button field" type="submit">Sign me in</button>
                    <div class="field center_aligned">
                        <div>If you have an account and forget your password, please
                            <nuxt-link to="/">reset it</nuxt-link>.
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    layout: 'base',
    data() {
        return {
            formUsername: '',
            formPassword: '',
            formErrors: {}
        };
    },
    methods: {
        async login() {
            try {
                await this.$store.dispatch('auth/login', {
                    username: this.formUsername,
                    password: this.formPassword
                });
            } catch (e) {
                let { data } = e.response;
                this.formErrors = data;
            }
        }
    }
};
</script>
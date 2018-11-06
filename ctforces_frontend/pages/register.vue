<template>
    <div class="ui segment">
        <div>Sign Up</div>
        <div class="ui clearing divider"></div>
        <form class="ui form error warning" @submit.prevent="register">
            <div class="field">
                <input type="text" name="username" placeholder="Handle" v-model="registerForm.username">
            </div>
            <div class="field">
                <input type="text" name="username" placeholder="Email" v-model="registerForm.email">
            </div>
            <div class="field">
                <input type="password" name="password1" placeholder="Password" v-model="registerForm.password1"/>
            </div>
            <div class="field">
                <input type="password" name="password2" placeholder="Repeat password" v-model="registerForm.password2"/>
            </div>
            <div v-if="registerForm.errors['detail']" class="ui error message">
                {{ registerForm.errors['detail'] }}
            </div>
            <button class="ui fluid teal button field" type="submit">Sign me up</button>
        </form>
    </div>
</template>

<script>
export default {
    layout: 'base',
    data() {
        return {
            registerForm: {
                username: '',
                email: '',
                password1: '',
                password2: '',
                errors: {}
            }
        };
    },
    methods: {
        async register() {
            try {
                if (
                    this.registerForm.password1 !== this.registerForm.password2
                ) {
                    this.registerForm.errors = {
                        detail: 'Passwords do not match'
                    };
                }
                let { data } = this.$axios.post('/register/', {
                    username: this.registerForm.username,
                    email: this.registerForm.email,
                    password: this.registerForm.password1
                });
                this.$router.push('/login/');
            } catch (e) {
                let { data } = e.response;
                this.registerForm.errors = data;
            }
        }
    }
};
</script>
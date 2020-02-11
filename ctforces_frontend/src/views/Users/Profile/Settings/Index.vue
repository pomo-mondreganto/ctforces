<template>
    <card>
        <f-header text="Settings" />
        <form class="def-form mt-3" @submit.prevent="updateSettings">
            <div class="ff">
                <f-input
                    type="password"
                    name="old_password"
                    v-model="oldPassword"
                    :errors="errors['old_password']"
                    placeholder="Old password"
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
                <input type="submit" value="Update" class="btn" />
            </div>
            <div class="ff">
                <f-detail :errors="errors['detail']" />
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
            oldPassword: null,
            password: null,
            errors: {},
        };
    },

    methods: {
        updateSettings: async function() {
            try {
                await this.$http.put('/me/', {
                    password: this.password,
                    old_password: this.oldPassword,
                });

                await this.$store.dispatch('UPDATE_USER');
                this.$router.push({ name: 'login' });
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

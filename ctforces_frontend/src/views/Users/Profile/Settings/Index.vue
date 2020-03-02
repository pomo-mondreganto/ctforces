<template>
    <card>
        <f-header text="Settings" />
        <form
            class="def-form mt-3"
            @submit.prevent="updateSettings"
            v-if="!$types.isNull(user)"
        >
            <div class="ff">
                <f-input
                    type="text"
                    name="username"
                    :value="user.username"
                    disabled
                />
            </div>
            <div class="ff">
                <f-input
                    type="email"
                    name="email"
                    :value="user.email"
                    disabled
                />
            </div>
            <div class="ff">
                <f-input
                    type="text"
                    name="first_name"
                    :value="personal_info.first_name"
                />
            </div>
            <div class="ff">
                <f-input
                    type="text"
                    name="last_name"
                    v-model="personal_info.last_name"
                />
            </div>
            <div class="ff">
                <f-input
                    type="text"
                    name="telegram"
                    v-model="personal_info.telegram"
                />
            </div>
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

import { mapState } from 'vuex';

export default {
    components: {
        FInput,
        Card,
        FHeader,
        FDetail,
    },

    data: function() {
        return {
            oldPassword: '',
            password: '',
            personal_info: {
                first_name: '',
                last_name: '',
                telegram: '',
            },
            errors: {},
        };
    },

    created: async function() {
        await this.$store.dispatch('GET_USER');

        this.personal_info = this.user.personal_info;
    },

    methods: {
        updateSettings: async function() {
            try {
                await this.$http.put('/me/', {
                    password: this.password,
                    old_password: this.oldPassword,
                    personal_info: this.personal_info,
                });

                await this.$store.dispatch('UPDATE_USER');
                if ((await this.$store.dispatch('GET_USER')) === null) {
                    this.$router.push({ name: 'login' }).catch(() => {});
                }
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: mapState(['user']),
};
</script>

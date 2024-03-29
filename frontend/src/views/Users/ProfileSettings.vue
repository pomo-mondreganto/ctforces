<template>
    <div>
        <f-header text="Settings" />
        <form @submit.prevent="updateAvatar" v-if="!$types.isNull(user)">
            <div class="ff">
                Change avatar:
                <input
                    name="avatar"
                    @change="changeAvatarFile($event.target.files)"
                    class="input file"
                    type="file"
                />
            </div>
            <div class="ff">
                <input type="submit" value="Update" class="btn" />
            </div>
        </form>
        <form @submit.prevent="updateSettings" v-if="!$types.isNull(user)">
            <f-detail :errors="errors['avatar']" />
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
                    placeholder="First name"
                    v-model="personalInfo.firstName"
                    :errors="errors['first_name']"
                />
            </div>
            <div class="ff">
                <f-input
                    type="text"
                    name="last_name"
                    placeholder="Last name"
                    v-model="personalInfo.lastName"
                    :errors="errors['last_name']"
                />
            </div>
            <div class="ff">
                <f-input
                    type="text"
                    name="telegram"
                    placeholder="Telegram"
                    v-model="personalInfo.telegram"
                    :errors="errors['telegram']"
                />
            </div>
            <div class="ff">
                <f-checkbox
                    name="hide_personal_info"
                    v-model="hidePersonalInfo"
                    label="Hide personal info"
                    :errors="errors['hide_personal_info']"
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
                <f-detail :errors="errors['detail']" />
            </div>
            <div class="ff">
                <input type="submit" value="Update" class="btn" />
            </div>
        </form>
    </div>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';
import FCheckbox from '@/components/Form/Checkbox';

import { mapState } from 'vuex';

export default {
    components: {
        FInput,
        FHeader,
        FCheckbox,
    },

    data: function() {
        return {
            oldPassword: '',
            password: '',
            hidePersonalInfo: false,
            personalInfo: {
                firstName: null,
                lastName: null,
                telegram: null,
            },
            errors: {},
            avatar: null,
        };
    },

    created: async function() {
        await this.$store.dispatch('GET_USER');

        this.personalInfo.firstName = this.user.personal_info.first_name;
        this.personalInfo.lastName = this.user.personal_info.last_name;
        this.personalInfo.telegram = this.user.personal_info.telegram;
    },

    methods: {
        changeAvatarFile: function(files) {
            this.avatar = files[0];
        },

        updateAvatar: async function() {
            if (this.$types.isNull(this.avatar)) {
                this.errors = {
                    avatar: ['No avatar selected'],
                };
                return;
            }
            let form = new FormData();
            form.set('name', this.avatar.name);
            form.append('avatar', this.avatar);
            try {
                await this.$http.post('/avatar_upload/', form);
                await this.$store.dispatch('UPDATE_USER');
                this.errors = {};
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        updateSettings: async function() {
            try {
                await this.$http.put('/me/', {
                    password: this.password,
                    old_password: this.oldPassword,
                    personal_info: {
                        first_name: this.personalInfo.firstName,
                        last_name: this.personalInfo.lastName,
                        telegram: this.personalInfo.telegram,
                    },
                    hide_personal_info: this.hidePersonalInfo,
                });

                this.$toasted.success('Changed!');

                await this.$store.dispatch('UPDATE_USER');
                if ((await this.$store.dispatch('GET_USER')) === null) {
                    this.$router.push({ name: 'login' }).catch(() => {});
                }

                this.errors = {};
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    computed: mapState(['user']),
};
</script>

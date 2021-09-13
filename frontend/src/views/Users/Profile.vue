<template>
    <master-layout>
        <tabs :tabs="tabs">
            <router-view />
        </tabs>
    </master-layout>
</template>

<script>
import Tabs from '@/components/Tabs';
import { mapState } from 'vuex';

export default {
    components: {
        Tabs,
    },

    computed: {
        ...mapState(['user']),
        tabs: function() {
            const username = this.$route.params.username;
            const result = [
                {
                    name: username,
                    to: {
                        name: 'profile',
                        params: { username },
                    },
                },
                {
                    name: 'Blog',
                    to: {
                        name: 'blog',
                        params: { username },
                    },
                },
                {
                    name: 'Tasks',
                    to: {
                        name: 'user_tasks',
                        params: { username },
                    },
                },
                {
                    name: 'Teams',
                    to: {
                        name: 'teams',
                        params: { username },
                    },
                },
            ];
            if (
                !this.$types.isNull(this.user) &&
                this.user.username === username
            ) {
                result.push({
                    name: 'Settings',
                    to: {
                        name: 'settings',
                        params: { username },
                    },
                });
            }
            return result;
        },
    },
};
</script>

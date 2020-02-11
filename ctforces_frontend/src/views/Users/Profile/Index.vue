<template>
    <tabs
        :tabs="[
            {
                name: $route.params.username,
                to: {
                    name: 'profile',
                    params: { username: $route.params.username },
                },
            },
            {
                name: 'Settings',
                to: {
                    name: 'settings',
                    params: { username: $route.params.username },
                },
            },
        ]"
    >
        <router-view />
    </tabs>
</template>

<script>
import Tabs from '@/components/Tabs/Index';

export default {
    components: {
        Tabs,
    },
};
</script>

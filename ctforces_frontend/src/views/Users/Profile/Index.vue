<template>
    <master-layout>
        <tabs
            :tabs="
                [
                    {
                        name: $route.params.username,
                        to: {
                            name: 'profile',
                            params: { username: $route.params.username },
                        },
                    },
                    {
                        name: 'Blog',
                        to: {
                            name: 'blog',
                            params: { username: $route.params.username },
                        },
                    },
                    {
                        name: 'Teams',
                        to: {
                            name: 'teams',
                            params: { username: $route.params.username },
                        },
                    },
                ].concat(
                    $types.isNull(user) ||
                        user.username !== $route.params.username
                        ? []
                        : [
                              {
                                  name: 'Settings',
                                  to: {
                                      name: 'settings',
                                      params: {
                                          username: $route.params.username,
                                      },
                                  },
                              },
                          ]
                )
            "
        >
            <router-view />
        </tabs>
    </master-layout>
</template>

<script>
import Tabs from '@/components/Tabs/Index';
import { mapState } from 'vuex';

export default {
    components: {
        Tabs,
    },

    computed: mapState(['user']),
};
</script>

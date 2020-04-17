<template>
    <div class="p-r">
        <div class="a-tr">
            <router-link :to="{ name: 'team_create' }" class="btn nlnk">
                Create team
            </router-link>
        </div>
        <f-header :text="`${$route.params.username} teams`" />
    </div>
</template>

<script>
import FHeader from '@/components/Form/Header';

export default {
    components: {
        FHeader,
    },
};
</script>

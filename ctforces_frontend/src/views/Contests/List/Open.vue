<template>
    <router-link :to="{ name: 'contest_tasks', params: { id: row.id } }">
        Open
    </router-link>
</template>

<script>
import { mapState } from 'vuex';

export default {
    props: {
        fieldData: String,
        row: Object,
    },

    computed: mapState(['user']),
};
</script>

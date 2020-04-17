<template>
    <router-link
        :to="{ name: 'contest_tasks', params: { id: row.id } }"
        v-if="(!$types.isNull(user) && user.is_admin) || row[fieldData]"
    >
        Open
    </router-link>
    <router-link
        :to="{ name: 'contest_register', params: { id: row['id'] } }"
        v-else
    >
        Register
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

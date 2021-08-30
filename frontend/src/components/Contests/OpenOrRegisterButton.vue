<template>
    <router-link
        class="link nlnk"
        :to="{ name: 'contest_info', params: { id: row.id } }"
        v-if="(!$types.isNull(user) && user.is_admin) || row[fieldData]"
    >
        Open
    </router-link>
    <div v-else-if="!row.is_registration_open">Closed</div>
    <router-link
        class="link nlnk register"
        :to="{ name: 'contest_register', params: { id: row.id } }"
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

<style lang="scss" scoped>
.register {
    @include use-theme {
        color: $green;
    }
    cursor: pointer;
}
</style>

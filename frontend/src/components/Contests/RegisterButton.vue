<template>
    <router-link
        class="link nlnk"
        v-if="!$types.isNull(user) && user.is_admin"
        :to="{ name: 'contest_info', params: { id: row.id } }"
    >
        Open
    </router-link>
    <div
        v-else-if="!$types.isNull(user) && row[fieldData]"
        class="unregister"
        @click="aux.unregister(row.id)"
    >
        Unregister
    </div>
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
        aux: Object,
    },

    computed: mapState(['user']),
};
</script>

<style lang="scss" scoped>
.unregister {
    @include use-theme {
        color: $reddanger;
    }
    cursor: pointer;
}

.register {
    @include use-theme {
        color: $green;
    }
    cursor: pointer;
}
</style>

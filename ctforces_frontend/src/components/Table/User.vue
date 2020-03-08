<template>
    <user :username="row['username']" :rating="row['rating']" />
</template>

<script>
import User from '@/components/User/Index';

export default {
    props: {
        fieldName: String,
        row: Object,
    },

    components: {
        User,
    },
};
</script>

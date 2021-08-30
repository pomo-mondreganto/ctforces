<template>
    <router-link
        :to="{ name: 'team_index', params: { id } }"
        class="link nlnk"
        >{{ name }}</router-link
    >
</template>

<script>
export default {
    props: {
        id: Number,
        name: String,
        rating: Number,
    },
};
</script>

<template>
    <div class="p-r">
        <div class="a-tr">
            <button type="button" @click="createTeam()" class="btn">
                Create team
            </button>
        </div>
        <div>Team list</div>
    </div>
</template>

<script>
export default {
    methods: {
        createTeam: function() {
            this.$router.push({ name: 'team_create' }).catch(() => {});
        },
    },
};
</script>

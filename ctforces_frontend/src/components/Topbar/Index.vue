<template>
    <div class="menu">
        <div class="logo vc" @click="indexRedirect">CTForces</div>
        <div class="navigation vc">
            <nav-button to="index" text="Home" />
            <nav-button to="contests" text="Contests" />
            <nav-button to="tasks" text="Tasks" />
            <nav-button to="upsolving" text="Upsolving" />
            <nav-button to="rating" text="Rating" />
        </div>
        <div class="logreg vc">
            <login-button />
            <register-button />
        </div>
    </div>
</template>

<script>
import LoginButton from './LoginButton';
import RegisterButton from './RegisterButton';
import NavButton from './NavButton';

export default {
    components: {
        LoginButton,
        RegisterButton,
        NavButton,
    },
    methods: {
        indexRedirect: function() {
            this.$router.push({ name: 'index' }).catch(() => {});
        },
    },
};
</script>

<style lang="scss" scoped>
.menu {
    display: flex;
    height: 4em;
    background-color: $light;
    box-shadow: 0 0.1em 0.3em #eeeeee;
    margin-bottom: 1.8em;
}

.logo {
    font-size: 1.5em;
    margin-left: 0.5em;
    flex-grow: 2;
    padding: 0.3em;
    cursor: pointer;
}

.navigation {
    flex-grow: 20;
}

.logreg {
    display: flex;
    flex-grow: 3;

    .btn {
        flex-grow: 1;
        flex-basis: 0;
    }

    .rb {
        margin-left: 0.5em;
    }

    margin-right: 0.5em;
}
</style>

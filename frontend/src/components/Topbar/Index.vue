<template>
    <div class="menu">
        <router-link :to="{ name: 'index' }" class="logo vc ml-0-5"
            >CTForces</router-link
        >
        <div class="navigation vc">
            <nav-button to="index" text="Home" />
            <nav-button to="contest_list" text="Contests" />
            <nav-button to="task_list" text="Tasks" />
            <nav-button to="upsolving" text="Upsolving" />
            <nav-button to="rating" text="Rating" />
        </div>
        <div class="theme vc">
            <svg
                @click="changeTheme"
                class="theme-img"
                height="576.409px"
                viewBox="0 0 576.41 576.409"
            >
                <g>
                    <path
                        d="M575.391,177.483c-8.801,10.27-18.997,9.354-29.011,5.667c-13.919-5.126-27.604-10.93-41.223-16.826
		c-33.546-14.523-68.137-23.306-105.074-20.64c-28.259,2.054-55.848,7.495-82.41,17.187c-9.892,3.603-19.688,5.646-29.47,6.094
		c-9.78-0.447-19.578-2.491-29.468-6.094c-26.561-9.687-54.151-15.132-82.413-17.187c-36.935-2.671-71.528,6.116-105.073,20.64
		c-13.617,5.9-27.305,11.699-41.223,16.826c-10.011,3.687-20.208,4.603-29.01-5.667c-3.37,53.865,1.028,105.223,22.478,154.106
		c12.553,28.609,30.311,53.35,56.17,71.285c41.837,29.006,87.425,36.068,135.737,19.651c10.669-3.625,20.249-10.892,29.81-17.244
		c15.117-10.055,30.311-17.001,43.44-17.001c13.128,0,27.408,6.946,42.531,17.001c9.566,6.362,19.144,13.619,29.812,17.244
		c48.312,16.407,93.907,9.354,135.734-19.651c25.862-17.936,43.614-42.676,56.167-71.285
		C574.36,282.706,578.768,231.348,575.391,177.483z M110.009,337.49c-47.334-24.699-57.927-97.952-57.927-97.952
		s60.829-23.016,108.158,1.674c47.334,24.699,63.246,87.757,63.246,87.757S157.344,362.179,110.009,337.49z M466.408,337.49
		c-47.332,24.688-113.478-8.521-113.478-8.521s15.919-63.058,63.246-87.757c47.337-24.689,108.161-1.674,108.161-1.674
		S513.739,312.791,466.408,337.49z"
                    />
                </g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
                <g></g>
            </svg>
        </div>
        <div class="logreg vc mr-0-5">
            <login-button />
            <register-logout />
            <hamburger />
        </div>
    </div>
</template>

<script>
import LoginButton from './LoginButton';
import RegisterLogout from './RegisterLogout';
import NavButton from './NavButton';
import Hamburger from './Hamburger';

export default {
    components: {
        LoginButton,
        RegisterLogout,
        NavButton,
        Hamburger,
    },

    data: function() {
        return {
            theme: null,
        };
    },

    created: function() {
        this.theme = localStorage.getItem('theme');
    },

    methods: {
        changeTheme: function() {
            if (this.$types.isNull(this.theme)) {
                localStorage.setItem('theme', 'dark-theme');
                document.body.classList.add('dark-theme');
                this.theme = 'dark-theme';
            } else {
                localStorage.removeItem('theme');
                this.theme = null;
                document.body.classList.remove('dark-theme');
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.menu {
    display: flex;
    height: 4em;
    @include use-theme {
        background-color: $light;
        box-shadow: 0 0.1em 0.3em $topbarshadow;
    }
    margin-bottom: 1.8em;
}

.logo {
    text-decoration: none;
    outline: none;
    @include use-theme {
        color: $black;
    }
    font-size: 1.5em;
    flex: 2 1 0;
    padding: 0.3em;
    cursor: pointer;
}

.navigation {
    flex: 10 1 0;
}

.theme {
    flex: 1 1 0;
    padding-right: 0.5em;
    .theme-img {
        cursor: pointer;
        @include use-theme {
            fill: rgba($black, 0.2);
        }
        max-height: 3.5em;
    }
}

.logreg {
    display: flex;
    flex: 3 1 0;

    @media only screen and (max-width: 991px) {
        flex: 2 1 0;
    }
}
</style>

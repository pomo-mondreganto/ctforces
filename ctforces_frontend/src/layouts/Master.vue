<template>
    <div id="app">
        <header>
            <topbar />
        </header>
        <container>
            <div class="layout">
                <slot />
                <div class="sidebar-wrapper">
                    <slot name="sidebar">
                        <sidebar />
                    </slot>
                </div>
            </div>
        </container>
        <footer class="ta-c mt-2">
            Powered by <span class="team">C4T BuT S4D</span> CTF team
        </footer>
    </div>
</template>

<script>
import Topbar from '@/components/Topbar/Index';
import Container from '@/components/Container/Index';
import Sidebar from '@/components/Sidebar/Index';

export default {
    components: {
        Topbar,
        Container,
        Sidebar,
    },
};
</script>

<style lang="scss" scoped>
#app {
    height: 100%;
    display: flex;
    flex-flow: column nowrap;

    & > :nth-child(2) {
        flex: 1 1 0;
    }

    .layout {
        @media only screen and (min-width: 992px) {
            display: flex;

            flex-flow: row nowrap;

            align-items: flex-start;

            & > :nth-child(1) {
                flex: 2.2 1 0;
                margin-right: 3em;
                min-width: 0;
            }

            & > :nth-child(2) {
                flex: 1 1 0;
                min-width: 0;
            }
        }

        @media only screen and (max-width: 991px) {
            & > :nth-child(1) {
                border: none;
                width: calc(100% - 2em);
            }

            & > :nth-child(2) {
                width: 100%;
            }
        }
    }
}

.team {
    font-size: 1.1em;
    font-weight: 900;
}
</style>

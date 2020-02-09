<template>
    <div id="app">
        <header>
            <topbar />
        </header>
        <container>
            <div class="layout">
                <slot />
                <sidebar />
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
        flex-grow: 1;
    }

    .layout {
        display: flex;
        flex-flow: row nowrap;

        & > :nth-child(1) {
            flex: 2.2 1 0;
            margin-right: 3em;
        }
    }
}

.team {
    font-size: 1.1em;
    font-weight: 900;
}
</style>

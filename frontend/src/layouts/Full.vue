<template>
    <div id="app">
        <header>
            <topbar />
        </header>
        <container>
            <div class="layout">
                <slot />
            </div>
        </container>
        <base-footer />
    </div>
</template>

<script>
import BaseFooter from '@/components/BaseFooter';
import Topbar from '@/components/Topbar/Index';
import Container from '@/components/Container';

export default {
    components: {
        Topbar,
        BaseFooter,
        Container,
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
}

.team {
    font-size: 1.1em;
    font-weight: 900;
}
</style>

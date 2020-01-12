<template>
    <fragment>
        <header>
            <topbar />
        </header>
        <container>
            <slot />
        </container>
        <footer class="tac">
            Powered by <span class="team">C4T BuT S4D</span> CTF team
        </footer>
    </fragment>
</template>

<script>
import Topbar from '@/components/Topbar/Index';
import Container from '@/components/Container/Index';

export default {
    components: {
        Topbar,
        Container,
    },
};
</script>

<style lang="scss" scoped>
.team {
    font-size: 1.1em;
    font-weight: 900;
}
</style>

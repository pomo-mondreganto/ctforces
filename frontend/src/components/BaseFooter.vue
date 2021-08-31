<template>
    <footer class="ta-c mt-2">
        Powered by
        <a class="team" href="https://cbsctf.ru/about-us">C4T BuT S4D</a> CTF
        team
    </footer>
</template>

<style lang="scss" scoped>
.team {
    font-size: 1.1em;
    font-weight: 900;
    padding-bottom: 0.5em;

    &:link,
    &:visited {
        @include use-theme {
            color: $black;
        }
    }
}
</style>

<template>
    <div>
        <Menu/>

        <div class="pusher">
            <div id="swipe-wrap">
                <div class="ui container">
                    <div class="ui segment">
                        <nuxt/>
                    </div>
                </div>
            </div>
            <footer class="footer">
                Powered by KekusCorporation.
            </footer>
        </div>
    </div>
</template>

<script>
import Menu from '~/components/Menu.vue';

export default {
    components: {
        Menu
    }
};
</script>

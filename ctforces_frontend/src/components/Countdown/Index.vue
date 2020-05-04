<template>
    <vue-countdown :time="Math.max(0, time)" v-slot="props" class="ta-c">
        <slot :time="props" />
    </vue-countdown>
</template>

<script>
import VueCountdown from '@chenfengyuan/vue-countdown';

export default {
    props: {
        time: Number,
    },

    components: {
        VueCountdown,
    },
};
</script>

<template>
    <div>
        <span class="link" v-if="!show" @click="change">Hint {{ num }}</span>
        <div v-else>
            <hr />
            <span @click="change" class="hint">Hint {{ num }}: {{ text }}</span>
            <hr />
        </div>
        <f-detail :errors="errors['detail']" />
    </div>
</template>

<script>
export default {
    props: {
        id: Number,
        num: Number,
    },

    data: function() {
        return {
            show: false,
            text: '',
            errors: {},
        };
    },

    methods: {
        change: async function() {
            if (!this.show) {
                try {
                    const r = await this.$http.get(`/task_hints/${this.id}/`);
                    this.text = r.data.body;
                } catch (error) {
                    this.errors = this.$parse(error.response.data);
                }
            }
            this.show = !this.show;
        },
    },
};
</script>

<style lang="scss" scoped>
.hint {
    cursor: pointer;
}
</style>

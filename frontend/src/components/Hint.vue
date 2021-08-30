<template>
    <div>
        <span v-if="!show" class="link" @click="change">Hint {{ num }}</span>
        <div v-else>
            <hr />
            <span class="hint" @click="change">Hint {{ num }}: {{ text }}</span>
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
                    const { data } = await this.$http.get(
                        `/task_hints/${this.id}/`
                    );
                    this.text = data.body;
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
    line-height: 1.2em;
}
</style>

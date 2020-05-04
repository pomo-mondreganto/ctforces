<template>
    <div class="tags jc-c">
        <tag v-for="tag of row[fieldData]" :key="tag.id" :name="tag.name" />
    </div>
</template>

<script>
import Tag from '@/components/Tag/Index';

export default {
    props: {
        fieldData: String,
        row: Object,
    },

    components: {
        Tag,
    },
};
</script>

<style lang="scss" scoped>
.tags {
    display: flex;
    flex-flow: row wrap;
}
</style>

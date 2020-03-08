<template>
    <div class="tags jc-c">
        <tag v-for="tag of row[fieldName]" :key="tag.id">
            {{ tag.name }}
        </tag>
    </div>
</template>

<script>
import Tag from '@/components/Tag/Index';

export default {
    props: {
        fieldName: String,
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

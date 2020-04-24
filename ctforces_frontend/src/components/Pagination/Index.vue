<template>
    <div
        v-if="!$types.isNull(count) && !$types.isNull(page) && pageCount > 1"
        class="pl-2 pr-2 mt-1"
    >
        <paginate
            v-model="page"
            :clickHandler="changePage"
            :page-count="pageCount"
            :page-range="5"
            container-class="pagination"
            page-class="page"
            prev-class="prev-page"
            next-class="next-page"
            page-link-class="page-link"
            prev-link-class="page-link"
            next-link-class="page-link"
            active-class="active"
        />
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            page: null,
        };
    },

    props: {
        count: Number,
        pagesize: Number,
    },

    methods: {
        changePage: function(page) {
            const query = Object.assign({}, this.$route.query, {
                page,
            });
            this.$router.push({ query }).catch(() => {});
        },
    },

    created: function() {
        let { page = '1' } = this.$route.query;
        page = parseInt(page);
        this.page = page;
    },

    computed: {
        pageCount: function() {
            return Math.max(
                1,
                Math.floor((this.count + this.pagesize - 1) / this.pagesize)
            );
        },
    },
};
</script>

<style lang="scss">
.pagination {
    width: 100%;
    display: flex;
    flex-flow: row nowrap;

    border: 1px solid $darklight;
    border-radius: 1em;

    .page,
    .prev-page,
    .next-page {
        flex: 1 1 0;

        list-style-type: none;

        display: flex;
        flex-flow: row nowrap;
        justify-content: center;

        &:not(:last-child) {
            border-right: 1px solid $gray;
        }

        &.active {
            background-color: $gray;
        }

        & .page-link {
            padding: 0.5em;
            width: 100%;
            text-align: center;
            outline: none;
        }
    }
}
</style>

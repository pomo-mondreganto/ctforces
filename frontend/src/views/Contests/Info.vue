<template
    ><div v-if="!$types.isNull(contest)">
        <div
            v-if="!$types.isNull(contest) && contest.can_edit_contest"
            class="p-r"
        >
            <div class="a-tr">
                <router-link
                    :to="{ name: 'contest_edit', params: { id: contest.id } }"
                    class="btn nlnk"
                >
                    Edit contest
                </router-link>
            </div>
        </div>
        <div class="header">
            {{ contest.name }}
        </div>
        <div class="mt-1-5">
            <span>By </span>
            <user
                :rating="contest.author_rating"
                :username="contest.author_username"
            />
        </div>
        <div class="hr mt-1" />
        <div class="content mt-1">
            <div class="markdown ml-1 p-1">
                <markdown :content="contest.description" />
            </div>
        </div></div
></template>

<script>
import Markdown from '@/components/Markdown';
import { mapState } from 'vuex';

export default {
    components: {
        Markdown,
    },
    computed: mapState('contests', ['contest']),
};
</script>

<style lang="scss" scoped>
.content {
    @include use-theme {
        border-left: 0.3em solid $gray;
    }
}

.header {
    font-size: 1.5em;
}
</style>

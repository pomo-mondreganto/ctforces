<template>
    <master-layout>
        <card>
            <div
                class="p-r"
                v-if="!$types.isNull(user) && user.can_create_contests"
            >
                <div class="a-tr">
                    <router-link
                        :to="{ name: 'contest_create' }"
                        class="btn nlnk"
                    >
                        Create contest
                    </router-link>
                </div>
            </div>
            <f-header
                text="Contests"
                v-if="
                    !(!$types.isNull(running) && running.length > 0) &&
                        !(!$types.isNull(upcoming) && upcoming.length > 0) &&
                        !(!$types.isNull(finished) && finished.length > 0)
                "
            />
            <f-header
                text="Running contests"
                v-if="!$types.isNull(running) && running.length > 0"
            />
            <div
                class="mt-1"
                v-if="!$types.isNull(running) && running.length > 0"
            >
                <f-table
                    :fields="[
                        {
                            name: '#',
                            pos: 'c',
                            grow: 1,
                        },
                        {
                            name: 'Name',
                            pos: 'l',
                            grow: 6,
                        },
                        {
                            name: 'Ends in',
                            pos: 'c',
                            grow: 3,
                            comp: TimerComp,
                            key: 'end_time',
                        },
                        {
                            name: '',
                            pos: 'c',
                            key: 'is_registered',
                            comp: OpenOrRegisterComp,
                            grow: 2,
                        },
                    ]"
                    :data="running"
                />
            </div>
            <f-header
                :class="
                    !$types.isNull(running) && running.length > 0 ? 'mt-1' : ''
                "
                text="Upcoming contests"
                v-if="!$types.isNull(upcoming) && upcoming.length > 0"
            />
            <div
                class="mt-1"
                v-if="!$types.isNull(upcoming) && upcoming.length > 0"
            >
                <f-table
                    :fields="[
                        {
                            name: '#',
                            pos: 'c',
                            grow: 1,
                        },
                        {
                            name: 'Name',
                            pos: 'l',
                            grow: 6,
                        },
                        {
                            name: 'Starts in',
                            pos: 'c',
                            grow: 3,
                            comp: TimerComp,
                            key: 'start_time',
                        },
                        {
                            name: '',
                            pos: 'c',
                            key: 'is_registered',
                            comp: RegisterComp,
                            grow: 2,
                            aux: {
                                unregister,
                            },
                        },
                    ]"
                    :data="upcoming"
                />
            </div>
            <f-header
                :class="
                    (!$types.isNull(running) && running.length > 0) ||
                    (!$types.isNull(upcoming) && upcoming.length > 0)
                        ? 'mt-1'
                        : ''
                "
                text="Finished contests"
                v-if="!$types.isNull(finished) && finished.length > 0"
            />
            <div
                class="mt-1"
                v-if="!$types.isNull(finished) && finished.length > 0"
            >
                <f-table
                    :fields="[
                        {
                            name: '#',
                            pos: 'c',
                            grow: 1,
                        },
                        {
                            name: 'Name',
                            pos: 'l',
                            grow: 9,
                        },
                        {
                            name: '',
                            pos: 'c',
                            comp: OpenComp,
                            grow: 2,
                        },
                    ]"
                    :data="finished"
                />
            </div>
            <f-detail :errors="errors['detail']" />
            <pagination :count="count" :pagesize="pagesize" />
        </card>
    </master-layout>
</template>

<script>
import FHeader from '@/components/Form/Header';
import FTable from '@/components/Table/Index';
import Pagination from '@/components/Pagination/Index';
import Timer from '@/components/Table/Timer';
import OpenOrRegister from '@/views/Contests/List/OpenOrRegister';
import Register from '@/views/Contests/List/Register';
import Open from '@/views/Contests/List/Open';
import { mapState } from 'vuex';

export default {
    components: {
        FHeader,
        FTable,
        Pagination,
    },

    data: function() {
        return {
            upcoming: null,
            running: null,
            finished: null,
            TimerComp: Timer,
            OpenOrRegisterComp: OpenOrRegister,
            RegisterComp: Register,
            OpenComp: Open,
            errors: {},
            count: null,
            pagesize: 20,
        };
    },

    methods: {
        unregister: async function(id) {
            try {
                const r = await this.$http.get(
                    `/contest_participant_relationship/?contest_id=${id}`
                );
                const { id: rid } = r.data[0];
                await this.$http.delete(
                    `/contest_participant_relationship/${rid}/`
                );
                await this.fetchContests();
                this.$toasted.success('Unregistered!');
            } catch (error) {
                this.$toasted.error(this.$parse(error.response.data).detail);
            }
        },

        fetchContests: async function() {
            const { page = 1 } = this.$route.query;
            try {
                const r = await this.$http.get(
                    `/contests/?page=${page}&page_size=${this.pagesize}`
                );
                this.upcoming = r.data.upcoming.map((contest, index) => {
                    return {
                        '#': index,
                        ...contest,
                    };
                });

                this.running = r.data.running.map((contest, index) => {
                    return {
                        '#': index,
                        ...contest,
                    };
                });

                this.finished = r.data.finished.results.map(
                    (contest, index) => {
                        return {
                            '#': index,
                            ...contest,
                        };
                    }
                );

                this.count = r.data.finished.count;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchContests();
    },

    watch: {
        async $route() {
            await this.fetchContests();
        },
    },

    computed: mapState(['user']),
};
</script>

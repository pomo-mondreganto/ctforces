<template>
    <master-layout>
        <card>
            <f-header
                text="Upcoming contests"
                v-if="!$types.isNull(upcoming) && upcoming.length > 0"
            />
            <div class="mt-1" v-if="!$types.isNull(upcoming)">
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
                            grow: 7,
                        },
                        {
                            Name: 'Starts in',
                            pos: 'c',
                            grow: 3,
                            comp: TimerComp,
                            key: 'start_time',
                        },
                        {
                            name: '',
                            pos: 'c',
                            key: 'is_registered',
                            comp: OpenOrRegisterComp,
                            grow: 2,
                        },
                    ]"
                    :data="upcoming"
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
            errors: {},
            count: null,
            pagesize: 20,
        };
    },

    methods: {
        fetchContests: async function() {
            const { page = 1 } = this.$route.query;
            try {
                const r = await this.$http.get(`/contests/?page=${page}`);
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
};
</script>

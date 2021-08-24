<template>
    <master-layout>
        <card>
            <div v-if="!$types.isNull(team)">
                <f-header :text="`Join team ${team.name}`" />
                <form class="mt-3" @submit.prevent="joinTeam">
                    <div class="ff">
                        <f-input
                            type="text"
                            name="join_token"
                            v-model="joinToken"
                            :errors="errors['join_token']"
                            placeholder="Token"
                        />
                    </div>
                    <div class="ff">
                        <f-detail :errors="errors['detail']" />
                    </div>
                    <div class="ff">
                        <input type="submit" value="Join team" class="btn" />
                    </div>
                </form>
            </div>
        </card>
    </master-layout>
</template>

<script>
import FInput from '@/components/Form/Input';
import FHeader from '@/components/Form/Header';

export default {
    components: {
        FInput,
        FHeader,
    },

    data: function() {
        return {
            joinToken: null,
            team: null,
            errors: {},
        };
    },

    methods: {
        joinTeam: async function() {
            const { id } = this.$route.params;
            try {
                await this.$http.post(`/teams/${id}/join/`, {
                    join_token: this.joinToken,
                });

                this.$router.push({
                    name: 'team_index',
                    params: { id },
                });
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },

        fetchTeam: async function() {
            const { id } = this.$route.params;
            try {
                const r = await this.$http.get(`/teams/${id}/`);
                this.team = r.data;
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },

    created: async function() {
        await this.fetchTeam();
    },

    watch: {
        $route: async function() {
            await this.fetchTeam();
        },
    },
};
</script>

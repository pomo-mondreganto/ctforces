<template>
    <master-layout>
        <card>
            <f-header text="Create team" />
            <form class="mt-3" @submit.prevent="createTeam">
                <div class="ff">
                    <f-input
                        type="text"
                        name="name"
                        v-model="name"
                        :errors="errors['name']"
                        placeholder="Name"
                    />
                </div>
                <div class="ff">
                    <f-detail :errors="errors['detail']" />
                </div>
                <div class="ff">
                    <input type="submit" value="Create team" class="btn" />
                </div>
            </form>
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
            name: null,
            errors: {},
        };
    },

    methods: {
        createTeam: async function() {
            try {
                const r = await this.$http.post('/teams/', {
                    name: this.name,
                });

                const { id } = r.data;

                this.$router.push({ name: 'team_index', params: { id } });
            } catch (error) {
                this.errors = this.$parse(error.response.data);
            }
        },
    },
};
</script>

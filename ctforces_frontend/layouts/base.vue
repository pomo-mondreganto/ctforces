<template>
    <div>
        <div class="ui container">
            <div class="ui bottom attached large nine item stackable menu">
                <div class="item">
                    <nuxt-link class="ui mini image" to="/">
                        <img src="~assets/img/logo.png" alt="">
                    </nuxt-link>
                </div>
                <nuxt-link class="item" to='/'>
                    <div>Home</div>
                </nuxt-link>
                <nuxt-link class="item" to="/contests">
                    <div>Contests</div>
                </nuxt-link>
                <nuxt-link class="item" to="/tasks">
                    <div>Tasks</div>
                </nuxt-link>
                <nuxt-link class="item" to="/users_upsolving">
                    <div>Upsolving</div>
                </nuxt-link>
                <nuxt-link class="item" to="/users_rating">
                    <div>Rating</div>
                </nuxt-link>

                <div v-if="authUser" class="right item">
                    <button class="ui primary button" to="/" style="white-space:nowrap;font-size:0.8em;">
                        {{ authUser.username }}
                    </button>
                </div>
                <div v-else class="right item">
                    <nuxt-link class="ui primary button" to="login" style="white-space:nowrap;font-size:0.8em;">
                        Sign In
                    </nuxt-link>
                </div>

                <div v-if="authUser" class="item">
                    <button class="ui button" @click="logout" style="white-space:nowrap;font-size:0.8em;">
                        Logout
                    </button>
                </div>
                <div v-else class="item">
                    <nuxt-link class="ui button" to="register" style="white-space:nowrap;font-size:0.8em;">
                        Sign Up
                    </nuxt-link>
                </div>
            </div>
        </div>

        <div class="pusher">
            <div id="swipe-wrap">
                <div class="ui container">
                    <div class="ui grid">
                        <div class="sixteen wide column">
                            <div class="ui basic vertical segment">
                                <nuxt/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <footer class="footer">
                Powered by KekusCorporation.
            </footer>
        </div>
    </div>
</template>

<script>
export default {
    computed: {
        authUser() {
            return this.$store.state.auth.authUser;
        }
    },
    methods: {
        async logout() {
            try {
                await this.$store.dispatch('auth/logout');
            } catch (e) {}
        }
    }
};
</script>

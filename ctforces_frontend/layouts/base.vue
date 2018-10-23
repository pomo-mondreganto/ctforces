<template>
    <div>
        <div class="ui container">
            <div class="ui bottom attached grid huge menu">
                <div class="one wide column item">
                    <a class="ui mini image" href="/">
                        <img src="~assets/img/logo.png" alt="">
                    </a>
                </div>
                <nuxt-link class="two wide column item center_aligned" to='/'>
                    <i class="fas fa-home"></i> <div style="padding-left: 3px">Home</div>
                </nuxt-link>
                <nuxt-link class="two wide column item center_aligned" to="/contests">
                    <i class="fas fa-chess-knight"></i> <div style="padding-left: 3px">Contests</div>
                </nuxt-link>
                <nuxt-link class="two wide column item center_aligned" to="/tasks">
                    <i class="fas fa-tasks"></i> <div style="padding-left: 3px">Tasks</div>
                </nuxt-link>
                <nuxt-link class="two wide column item center_aligned" to="/users_upsolving">
                    <i class="fas fa-check-circle"></i> <div style="padding-left: 3px">Upsolving</div>
                </nuxt-link>
                <nuxt-link class="two wide column item center_aligned" to="/users_rating">
                    <i class="fas fa-chess-king"></i> <div style="padding-left: 3px">Rating</div>
                </nuxt-link>

                    <div class="right item center_aligned">
                        <div class="menu_item_in">
                            <nuxt-link class="ui primary button" to="login">
                                Sign In
                            </nuxt-link>
                        </div>
                    </div>
                    <div class="item center_aligned">
                        <div class="menu_item_in">
                            <nuxt-link class="ui button" to="register">
                                Sign Up
                            </nuxt-link>
                        </div>
                    </div>
                <!--{% else %}
                    <div class="right item center_aligned">
                        <a class="ui primary button" href="{% url 'user_info' request.user.username %}">
                            username
                        </a>
                    </div>
                    <div class="item center_aligned">
                        <div class="menu_item_in">
                            <a class="ui button" href="{% url 'logout' %}">
                                Logout
                            </a>
                        </div>
                    </div>                
                {% endif %}-->
            </div>
        </div>

        <div class="pusher">
            <div id="swipe-wrap">
                <nuxt/>
            </div>
            <footer class="footer center_aligned">
                Powered by KekusCorporation.
            </footer>
        </div>
    </div>
</template>
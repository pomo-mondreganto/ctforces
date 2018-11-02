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
                <div class="right item">
                    <nuxt-link class="ui primary button" to="login" style="white-space:nowrap;font-size:0.8em;">
                        Sign In
                    </nuxt-link>
                </div>
                <div class="item">
                    <nuxt-link class="ui button" to="register" style="white-space:nowrap;font-size:0.8em;">
                        Sign Up
                    </nuxt-link>
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
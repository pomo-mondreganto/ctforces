const routes = require('next-routes');

module.exports = routes()
    .add('index', '/', 'index')
    .add('login', '/login', 'login')
    .add('register', '/register', 'register')
    .add('user_index', '/user/:username', 'user')
    .add('post_create', '/post/create', 'post/create')
    .add('post_index', '/post/:id', 'post/index')
    .add('post_edit', '/post/:id/edit', 'post/edit')
    .add('settings_general', '/settings/general', 'settings/general')
    .add('settings_social', '/settings/social', 'settings/social');

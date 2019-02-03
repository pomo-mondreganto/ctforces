const express = require('express');
const next = require('next');
const routes = require('./routes');

const dev = process.env.NODE_ENV !== 'production';
const PORT = process.env.PORT || 8080;

const app = next({ dir: '.', dev });
const handler = routes.getRequestHandler(app);

app.prepare().then(() => {
    express()
        .use(handler)
        .listen(8080);
});

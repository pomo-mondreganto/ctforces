const express = require('express');
const next = require('next');

const dev = process.env.NODE_ENV !== 'production';
const PORT = process.env.PORT || 3000;

const app = next({ dir: '.', dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
    const server = express();

    server.get('/', (req, res) => {
        return app.render(req, res, '/', req.query);
    });

    server.get('/login', (req, res) => {
        return app.render(req, res, '/login', req.query);
    });

    server.get('/register', (req, res) => {
        return app.render(req, res, '/register', req.query);
    });

    server.get('/profile', (req, res) => {
        return app.render(req, res, '/profile', req.query);
    });

    server.get('/users/:username', (req, res) => {
        const actualPage = '/user';
        const queryParams = { username: req.params.username };
        app.render(req, res, actualPage, queryParams);
    });

    server.get('/post/create', (req, res) => {
        return app.render(req, res, '/post/create', req.query);
    });

    server.get('/post/:id', (req, res) => {
        const actualPage = '/post';
        const queryParams = { id: req.params.id };
        app.render(req, res, actualPage, queryParams);
    });

    server.get('*', (req, res) => {
        return handle(req, res);
    });

    server.listen(PORT, err => {
        if (err) throw err;
        console.log(`> Ready on ${PORT}`);
    });
});

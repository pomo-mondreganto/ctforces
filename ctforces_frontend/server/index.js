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

    server.get('*', (req, res) => {
        return handle(req, res);
    });

    server.listen(PORT, err => {
        if (err) throw err;
        console.log(`> Ready on ${PORT}`);
    });
});

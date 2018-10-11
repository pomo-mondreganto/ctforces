import express from 'express';
import consola from 'consola';
// noinspection ES6CheckImport
import {Builder, Nuxt} from 'nuxt';
import config from '../nuxt.config.js';

const app = express();

const host = config.server.host;
const port = config.server.port;

app.set('port', port);

/* global process */

const dev = !(process.env.NODE_ENV === 'production');

async function start() {
  const nuxt = new Nuxt(config);

  if (dev) {
    const builder = new Builder(nuxt);
    await builder.build();
  }

  app.use(nuxt.render);

  app.listen(port, host);
  // noinspection JSUnresolvedFunction
  consola.ready({
    message: `Server listening on http://${host}:${port}`,
    badge: true
  });
}
start();

import pkg from './package';


// noinspection JSUnusedGlobalSymbols
export default {
  mode: 'universal',
  server: {
    port: 8000,
    host: '0.0.0.0',
  },
  head: {
    title: pkg.name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  loading: { color: '#fff' },
  css: [
  ],
  plugins: [
  ],
  modules: [
    '@nuxtjs/axios'
  ],
  axios: {
  },
  build: {
    extend(config, ctx) {

    }
  }
};

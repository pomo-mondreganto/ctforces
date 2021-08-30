FROM node:14-alpine as build

WORKDIR /app
COPY frontend/package.json .
COPY frontend/yarn.lock .
RUN yarn install

COPY frontend .
RUN yarn build

FROM nginx:1.21.1-alpine

COPY ./configs/nginx/proxy_params /etc/nginx/proxy_params
COPY ./configs/nginx/app.conf /etc/nginx/conf.d/default.conf
COPY ./configs/nginx/robots.txt /robots.txt
COPY --from=build /app/dist /front

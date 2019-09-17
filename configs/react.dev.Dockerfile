FROM node:11.9.0-alpine

RUN mkdir /app
ADD ./ctforces_react/package.json /app/package.json
ADD ./ctforces_react/package-lock.json /app/package-lock.json
WORKDIR /app
RUN npm install

ADD ./ctforces_react/ /app

ADD ./configs/react.dev.start.sh entrypoint.sh
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]

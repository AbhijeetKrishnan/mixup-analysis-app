# syntax=docker/dockerfile:1

FROM node:latest

WORKDIR /frontend

COPY package*.json .

RUN rm -rf node_modules
RUN rm -rf build
RUN npm install --omit=dev

EXPOSE 3000

COPY . .

RUN npm run build

ENTRYPOINT [ "ORIGIN=http://localhost:3000", "node", "build" ]
# syntax=docker/dockerfile:1

FROM node:latest

WORKDIR /frontend

COPY package*.json .

RUN rm -rf node_modules
RUN rm -rf build
RUN npm ci --omit=dev

COPY . .

RUN npm run build

ENTRYPOINT [ "node", "build" ]
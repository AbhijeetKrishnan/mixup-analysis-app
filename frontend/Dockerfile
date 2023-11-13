# syntax=docker/dockerfile:1

FROM node:latest

WORKDIR /frontend

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

ENTRYPOINT [ "node", "build" ]

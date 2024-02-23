FROM node:lts-alpine AS global-deps-stage
RUN npm i -g @quasar/cli@latest

FROM global-deps-stage AS develop-stage
WORKDIR /src
COPY package.json ./
COPY package-lock.json ./
COPY . .

FROM develop-stage AS local-deps-stage
RUN npm i

FROM local-deps-stage AS build-ssr-stage
RUN quasar build -m ssr

FROM local-deps-stage AS build-pwa-stage
RUN quasar build -m pwa

FROM node:lts-alpine AS prod-ssr-stage
WORKDIR /app
COPY --from=build-ssr-stage /src/dist/ssr .
RUN npm i -g serve
EXPOSE 3000
CMD ["node", "index.js"]

FROM nginx:stable-alpine AS prod-pwa-stage
WORKDIR /app
COPY --from=build-pwa-stage /src/dist/pwa /usr/share/nginx/html.
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

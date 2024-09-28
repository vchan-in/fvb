FROM node:18.0-alpine3.15 AS global-deps-stage
ARG FVB_BACKEND_BASEURL
ARG FVB_BACKEND_PORT
RUN npm i -g @quasar/cli@latest

FROM global-deps-stage AS develop-stage
WORKDIR /src
COPY package.json ./
COPY package-lock.json ./
COPY . .

FROM develop-stage AS local-deps-stage
RUN yarn install

FROM local-deps-stage AS build-pwa-stage
RUN FVB_BACKEND_BASEURL=${FVB_BACKEND_BASEURL} FVB_BACKEND_PORT=${FVB_BACKEND_PORT} quasar build -m pwa

FROM nginx:stable-alpine AS prod-pwa-stage
WORKDIR /app
COPY --from=build-pwa-stage /src/dist/pwa /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

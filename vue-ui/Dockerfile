FROM node:14 as build-stage
WORKDIR /build
COPY package*.json ./
RUN npm install
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /build/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
